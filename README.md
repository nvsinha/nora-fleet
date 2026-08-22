<!-- pyml disable no-inline-html,first-line-heading -->
<img src="https://raw.githubusercontent.com/nvsinha/nora-fleet/main/docs/logo.svg"
     alt="" width="72" height="72" />

<!-- pyml enable no-inline-html,first-line-heading -->

# Nora Fleet

**Multi-agent networks, defined in config.**

Nora Fleet is the runtime for agent networks that are declared in HOCON rather than written in
code. Run it as a library, or serve it over HTTP or gRPC.

## Why networks rather than one agent

Handing an entire complex task to a single model is the most common way to be disappointed by
one. The scope is usually wider than any one model can hold, and the gap between what people
expect and what they get is largely a gap of scope, not of capability.

Splitting the task changes that. A network of narrower agents, each with a job it can actually
do, can pass work between them and arrive somewhere a single prompt would not.

Nora Fleet networks are specified entirely as data, in
[HOCON](https://github.com/lightbend/config/blob/main/HOCON.md) — JSON with comments, among
other conveniences. That matters for who gets to build one: authoring a network becomes an
editing task, so subject matter experts can write them without going through a programmer.

Where a network needs to do something a language model cannot — query a web service, change
something through an API, handle private data correctly, perform exact arithmetic, move large
volumes of data without transcription errors — it calls a **coded tool**, written against
LangChain's interface or this project's own. That part does take programming. What it buys is
a way to compose the two halves of a problem: the parts that suit natural language, and the
parts that need deterministic code.

## What it provides

### Data handling

- `sly_data`, a side channel for private values that must stay out of LLM chat streams
- Security by default: you declare explicitly what is shared upstream and downstream
- Secure bring-your-own-key support, so client-supplied API keys let a deployment avoid
  carrying everyone else's token costs

### Model selection

- Provider-agnostic, with new LLMs configurable as data rather than code
- Per-agent model choice, so cost, latency, context window and data-residency can be traded
  off separately for each agent
- Fallback specifications for when a preferred provider is unavailable

### Operating it

- Detailed debugging output for understanding what a multi-agent system actually did
- Observability and tracing feeds for LangSmith, Langfuse, Arize Phoenix and HoneyHive
- Cloud-agnostic and ready to serve at scale, wherever you choose to run it
- Distributed agent webs, letting networks call each other across hosts
- An MCP protocol API — any Nora Fleet server can act as an MCP server
- Optional per-user authorization for agent networks, with an OpenFGA implementation available

### Testing

- Data-driven test cases
- The ability to have LLMs exercise your networks
- An Assessor application that classifies how an agent failed, given a data-driven case

## Quick start

The quickest route is the setup scripts, which handle everything below automatically:

```bash
# macOS and Linux
./quick-start/start-server.sh

# Windows
quick-start\start-server.bat
```

They create and activate a virtual environment, install dependencies, set environment
variables, enable CORS for web applications, and launch the server. See
[quick-start/README.md](quick-start/README.md) for the details.

You need Python 3.12 or later, with virtual environment support — normally included with
Python 3.12 and up.

To set things up by hand instead, continue below.

## Manual setup

Set `PYTHONPATH`, then create and activate a virtual environment:

```bash
export PYTHONPATH=$(pwd)
python3 -m venv venv
. ./venv/bin/activate
```

Install Nora Fleet. It is not published to PyPI, so it comes from the repository:

```bash
pip install "nora-fleet @ git+https://github.com/nvsinha/nora-fleet@v0.1.0"
```

Working from a clone of this repository, install the pinned dependencies instead:

```bash
pip install -r requirements.txt
```

At minimum, an API key for your model provider must be set. Add the equivalent variable for
any other provider your networks use:

```bash
export OPENAI_API_KEY="XXX_YOUR_OPENAI_API_KEY_HERE"
```

## Running

### As a library

From the top level of the repository:

```bash
python -m nora_fleet.client.agent_cli --agent hello_world
```

Give the chat client this:

```text
From earth, I approach a new planet and wish to send a short 2-word greeting to the new orb.
```

You should get back something along the lines of `Hello, world.` — though these are language
models, so expect variation.

### As a service

Start the server in the same terminal, with the environment variables above already set.
Running the service directly is usually the most convenient during development:

```bash
python -m nora_fleet.service.main_loop.server_main_loop
```

Alternatively, build and run the container:

```bash
./nora_fleet/deploy/build.sh ; ./nora_fleet/deploy/run.sh
```

The `build.sh`, `Dockerfile` and `run.sh` scripts are written to be portable, so they can be
pointed at your own registries and coded tools.

The container needs `OPENAI_API_KEY`, `AGENT_TOOL_PATH`, `AGENT_MANIFEST_FILE` and
`PYTHONPATH` passed through to it. Export them before running `run.sh`, or set them inside the
script.

Then connect a client from another terminal:

```bash
python -m nora_fleet.client.agent_cli --http --agent hello_world
```

### Notes on the chat client

`--help` documents the full set of arguments. A few points that are easy to trip over:

- The client cannot enumerate the agents registered with a service. This is deliberate.
- A newline sends the message, which makes pasting multi-line input awkward. Use
  `--first_prompt_file` to supply a file as the opening message instead.
- Private data that should stay out of the chat stream is passed as a single escaped JSON
  object: `--sly_data "{ \"login\": \"your_login\" }"`

## Building agent networks

### The example networks

The HOCON files under `./nora_fleet/registries` are working examples. To try one, pass its
filename stem to `--agent` on the chat client. Roughly in order of complexity:

- **hello_world** — the example used above. A front-man agent talking to one agent downstream.
- **esp_decision_assistant** — abstract, and considerably more capable. A front-man agent
  gathers the shape of a decision in ESP terms, then calls a prescriptor, which calls one or
  more predictors, arriving at a decision in an LLM-based ESP manner.

Every new HOCON file in that directory also needs an entry in `manifest.hocon`. After adding
one, rebuild and restart the service as above, then reach it through the chat client using its
file stem as the agent name.

### Further examples

The networks kept in this repository are deliberately spare — they exist for testing and for
demonstrating single ideas. For a fuller library of networks, along with documentation and
tutorials, see [nora-studio](https://github.com/nvsinha/nora-studio).

Every key available in an agent network is documented in the
[agent HOCON reference](docs/agent_hocon_reference.md).

### The manifest

Every agent in use needs an entry in one manifest file. In this repository that file is
`nora_fleet/registries/manifest.hocon`.

Your own agents will live in your own repository with their own manifest. Point Nora Fleet at
it with:

```bash
export AGENT_MANIFEST_FILE=<your_repo>/registries/manifest.hocon
```

## The AgentSession interface

Whether Nora Fleet runs as a library or as an HTTP service, both client and server reach
agents through
[AgentSession](https://github.com/nvsinha/nora-fleet/blob/main/nora_fleet/interfaces/agent_session.py).
It has two methods that matter:

`function()` reports what the top-level agent will do for the caller.

`streaming_chat()` is the main entry point. Send text and it opens a conversation with a
front-man agent. If that agent needs more from you it will ask, and you answer with another
call. Results stream back as `ChatMessage` values of several types, and the stream closes once
the conversation ends. Messages of type `AI` are the front man replying on behalf of the rest
of the network — those are the ones to read.

Two implementations ship:

- `DirectAgentSession` — for calling Nora Fleet as a library
- `HttpServiceAgentSession` — for calling a Nora Fleet HTTP service as a client

`agent_cli` uses both, so its source is a reasonable worked example.

Asynchronous implementations of
[AsyncAgentSession](https://github.com/nvsinha/nora-fleet/blob/main/nora_fleet/interfaces/async_agent_session.py)
are also available.

## Coded tools

Most examples here are no-code networks, but agent networks also support coded tools for
low-code solutions. They most often exist to call a specific web service, though they can be
any Python at all, provided they derive from the `CodedTool` interface in
`nora_fleet/interfaces/coded_tool.py`.

The interface centres on one method:

```python
async def async_invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Any:
```

A synchronous version exists for quick experiments, but the asynchronous form is the intended
entry point: Nora Fleet runs in an asynchronous server environment specifically so agents can
work in parallel.

`args` is supplied by the calling LLM, and its keys are defined in that tool's entry in the
agent's HOCON file.

`sly_data` is for values that must never reach the chat stream. Usually that means private
data, but it also works as a noticeboard where coded tools leave results for one another. It
can arrive from several directions:

- sent explicitly by a client — usernames, tokens, session identifiers and the like
- produced by other coded tools
- produced by other agent networks

The class and method comments in `nora_fleet/interfaces/coded_tool.py` go further.

Writing your own coded tools brings one more environment variable into play:

```bash
export AGENT_TOOL_PATH=<your_repo>/coded_tools
```

Below that path, classes are resolved dynamically by agent name, so a new tool belongs at:

```text
<your_repo>/coded_tools/<your_agent_name>/<your_coded_tool>.py
```

## Tests

Running the Python unit and integration tests is covered in [docs/tests.md](docs/tests.md).

## Writing clients

Building your own client is covered in [docs/clients.md](docs/clients.md).

## MCP protocol API

Using Nora Fleet as an MCP server is covered in [docs/mcp_service.md](docs/mcp_service.md).
