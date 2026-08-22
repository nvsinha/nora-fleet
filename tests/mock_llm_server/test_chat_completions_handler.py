# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
"""
Tests that the mock LLM server cannot be talked into emitting HTML.

CodeQL raised py/reflective-xss here: the handler echoes request-supplied tool
and model names straight back to the caller. The file already reached for
html.escape, but applied it to the values rather than to the bytes, which both
missed the point and corrupted the data -- a tool named "a&b" came back to
every client, browser or not, as "a&amp;b".

The escaping now happens once, on the serialized output. These tests pin both
halves of that: nothing renderable survives to the wire, and what does arrive
still decodes to exactly what was sent.
"""
# Fixture parameters intentionally share the fixture's name (standard pytest).
# pylint: disable=redefined-outer-name
import json
from typing import Any
from typing import Dict
from typing import List

import pytest
import tornado.httpclient
import tornado.httpserver
import tornado.web
from tornado.testing import bind_unused_port

from tests.mock_llm_server.chat_completions_handler import ChatCompletionsHandler
from tests.mock_llm_server.chat_completions_handler import _safe_json
from tests.mock_llm_server.mock_state import MockState

CHAT_PATH = "/v1/chat/completions"

# A name that is both a valid tool name and a complete HTML injection.
HOSTILE_NAME = '</script><script>alert(1)</script>'

# A name with a single ampersand: harmless, and the case html.escape silently
# rewrote for everyone.
AMPERSAND_NAME = "search_a&b"


@pytest.fixture
def start_app():
    """Bind the mock server to an unused loopback port and return its base URL."""
    servers: List[tornado.httpserver.HTTPServer] = []

    def _start() -> str:
        # Zero latencies keep the tests fast; the response text is irrelevant
        # here, since every assertion is about the tool and model names.
        state = MockState(
            responses=["ok"],
            min_latency=0.0,
            max_latency=0.0,
            model_name="mock-model",
            stream_token_delay=0.0,
        )
        app = tornado.web.Application([(CHAT_PATH, ChatCompletionsHandler, {"state": state})])
        sock, port = bind_unused_port()
        server = tornado.httpserver.HTTPServer(app)
        server.add_socket(sock)
        servers.append(server)
        return f"http://127.0.0.1:{port}"

    try:
        yield _start
    finally:
        for server in servers:
            server.stop()


def _tools(name: str) -> List[Dict[str, Any]]:
    """One OpenAI-shaped tool declaration carrying the given name."""
    return [{"type": "function", "function": {"name": name, "parameters": {}}}]


async def _post(url: str, payload: Dict[str, Any], stream: bool = False):
    """POST JSON; when streaming, accumulate the SSE body."""
    client = tornado.httpclient.AsyncHTTPClient(force_instance=True)
    chunks = bytearray()
    response = await client.fetch(
        f"{url}{CHAT_PATH}",
        method="POST",
        body=json.dumps({**payload, "stream": stream}),
        headers={"Content-Type": "application/json"},
        streaming_callback=(chunks.extend if stream else None),
        request_timeout=30,
        raise_error=False,
    )
    return response, (bytes(chunks) if stream else response.body)


def _sse_payloads(body: bytes) -> List[Dict[str, Any]]:
    """Parse the JSON out of every `data:` frame except the [DONE] sentinel."""
    out = []
    for line in body.decode().splitlines():
        if line.startswith("data: ") and line != "data: [DONE]":
            out.append(json.loads(line[len("data: "):]))
    return out


class TestSafeJson:
    """Unit tests for the serializer every response goes through."""

    def test_html_characters_never_reach_the_output(self):
        """The three characters that can begin a tag or entity are escaped."""
        wire = _safe_json({"name": HOSTILE_NAME, "note": "1 < 2 & 3 > 0"})
        for char in "<>&":
            assert char not in wire

    def test_escaping_is_lossless(self):
        """
        The output still decodes to exactly the input.

        This is the property html.escape did not have, and the reason the
        escaping moved from the values to the serialized form.
        """
        payload = {"name": HOSTILE_NAME, "model": AMPERSAND_NAME, "n": 1, "ok": True}
        assert json.loads(_safe_json(payload)) == payload

    def test_output_is_valid_json(self):
        """The escapes used are JSON's own, not an HTML entity encoding."""
        assert "\\u003c" in _safe_json({"a": "<"})
        assert json.loads(_safe_json({"a": "<"})) == {"a": "<"}


class TestHandlerResponses:
    """The escaping holds through the real handler, on both response shapes."""

    @pytest.mark.asyncio
    async def test_one_shot_response_carries_no_html(self, start_app):
        """A hostile tool name comes back inert and declared as JSON."""
        url = start_app()
        response, body = await _post(url, {"model": "m", "messages": [], "tools": _tools(HOSTILE_NAME)})

        assert response.code == 200
        assert b"<script" not in body
        assert response.headers["Content-Type"].startswith("application/json")
        assert response.headers["X-Content-Type-Options"] == "nosniff"

    @pytest.mark.asyncio
    async def test_streamed_response_carries_no_html(self, start_app):
        """The same holds for every SSE frame."""
        url = start_app()
        response, body = await _post(
            url, {"model": "m", "messages": [], "tools": _tools(HOSTILE_NAME)}, stream=True
        )

        assert response.code == 200
        assert b"<script" not in body
        assert response.headers["Content-Type"].startswith("text/event-stream")
        assert response.headers["X-Content-Type-Options"] == "nosniff"

    @pytest.mark.asyncio
    async def test_hostile_name_still_decodes_intact(self, start_app):
        """
        Inert on the wire, unchanged to a JSON client.

        A mock server that quietly rewrites what it echoes would make the load
        tests that depend on it lie.
        """
        url = start_app()
        _, body = await _post(
            url, {"model": "m", "messages": [], "tools": _tools(HOSTILE_NAME)}, stream=True
        )
        names = [
            call["function"]["name"]
            for payload in _sse_payloads(body)
            for call in payload["choices"][0]["delta"].get("tool_calls", [])
            if "name" in call.get("function", {})
        ]
        assert names == [HOSTILE_NAME]

    @pytest.mark.asyncio
    async def test_ampersand_in_a_name_is_not_rewritten(self, start_app):
        """
        "search_a&b" survives as itself.

        Under html.escape it became "search_a&amp;b" for every caller. This is
        the regression that fix introduced and this one removes.
        """
        url = start_app()
        _, body = await _post(
            url, {"model": "m", "messages": [], "tools": _tools(AMPERSAND_NAME)}, stream=True
        )
        names = [
            call["function"]["name"]
            for payload in _sse_payloads(body)
            for call in payload["choices"][0]["delta"].get("tool_calls", [])
            if "name" in call.get("function", {})
        ]
        assert names == [AMPERSAND_NAME]
        assert b"&amp;" not in body

    @pytest.mark.asyncio
    async def test_model_name_is_echoed_intact(self, start_app):
        """The model name is echoed too, and gets the same treatment."""
        url = start_app()
        _, body = await _post(url, {"model": AMPERSAND_NAME, "messages": []})
        assert json.loads(body)["model"] == AMPERSAND_NAME
