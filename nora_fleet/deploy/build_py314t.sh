#!/bin/bash -e

# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

# Builds the free-threaded (Python 3.14t) nora-fleet server container.
#
# All Python dependencies -- including the in-house nora-common --
# come from requirements.txt (i.e. from PyPI), so no
# sibling source repositories are needed. We still assemble a small, clean
# temporary build context (requirements.txt + the nora_fleet app source) rather
# than using the repo root directly, to keep the otherwise huge,
# scratch-file-laden nora-fleet working tree out of the build context.
#
# Usage:
#   ./nora_fleet/deploy/build_py314t.sh [--no-cache]
#
# Run it from the top-level directory of the nora-fleet repo.
#
# Overridable via environment:
#   SERVICE_TAG / SERVICE_VERSION   image name/tag components
#   TARGET_PLATFORM          docker build target platform (default: linux/amd64)
#   PYTHON_VERSION           free-threaded interpreter to provision via uv
#                            (default: 3.14t -- the trailing "t" selects no-GIL)
#   BASE_IMAGE               OS base for both stages (default: debian:trixie-slim)
#   UV_IMAGE                 image to lift the uv binary from
#                            (default: ghcr.io/astral-sh/uv:latest)
#
# NOTE: There is no official `python:3.14t` Docker image (the library/python
# repo publishes no free-threaded tags), so this build provisions the
# free-threaded interpreter with uv rather than via a base image.

export SERVICE_TAG=${SERVICE_TAG:-nora-fleet}
export SERVICE_VERSION=${SERVICE_VERSION:-0.0.1-py314t}

PYTHON_VERSION=${PYTHON_VERSION:-3.14t}
BASE_IMAGE=${BASE_IMAGE:-debian:trixie-slim}
UV_IMAGE=${UV_IMAGE:-ghcr.io/astral-sh/uv:latest}
echo ">>>>>>>>>>>>>>UV_IMAGE = ${UV_IMAGE}"

# Where this repo's app source and Dockerfile live, relative to the run dir.
NORA_FLEET_PKG="nora_fleet"
DOCKERFILE="${NORA_FLEET_PKG}/deploy/Dockerfile.py314t"

function build_main() {

    # Parse for a specific arg when debugging
    CACHE_OR_NO_CACHE="--rm"
    if [[ "${1:-}" == "--no-cache" ]]; then
        CACHE_OR_NO_CACHE="--no-cache --progress=plain"
    fi

    if [ -z "${TARGET_PLATFORM}" ]; then
        TARGET_PLATFORM="linux/amd64"
    fi
    echo "Target Platform for Docker image generation: ${TARGET_PLATFORM}"

    # Sanity checks on inputs
    if [ ! -d "${NORA_FLEET_PKG}" ]; then
        echo "ERROR: run this from the top-level of the nora-fleet repo (no ./${NORA_FLEET_PKG} here)." >&2
        exit 1
    fi
    if [ ! -f "${NORA_FLEET_PKG}/deploy/Dockerfile.py314t" ]; then
        echo "ERROR: ${NORA_FLEET_PKG}/deploy/Dockerfile.py314t not found." >&2
        exit 1
    fi
    # Assemble a clean, minimal build context in a temp dir.
    CTX=$(mktemp -d)
    # shellcheck disable=SC2064
    trap "rm -rf '${CTX}'" EXIT
    echo "Assembling build context in ${CTX}"

    # App source + runtime requirements.
    cp "requirements.txt" "${CTX}/requirements.txt"
    _copy_tree "${NORA_FLEET_PKG}" "${CTX}/${NORA_FLEET_PKG}"

    # Build the docker image.
    # DOCKER_BUILDKIT gives us modern build behavior.
    # shellcheck disable=SC2086
    DOCKER_BUILDKIT=1 docker build \
        -t nora-fleet/${SERVICE_TAG}:${SERVICE_VERSION} \
        --platform ${TARGET_PLATFORM} \
        --build-arg NORA_FLEET_VERSION="${USER}-$(date +'%Y-%m-%d-%H-%M')" \
        --build-arg PYTHON_VERSION="${PYTHON_VERSION}" \
        --build-arg BASE_IMAGE="${BASE_IMAGE}" \
        --build-arg UV_IMAGE="${UV_IMAGE}" \
        --build-arg PACKAGE_INSTALL="/usr/local/nora-fleet/myapp" \
        -f "${DOCKERFILE}" \
        ${CACHE_OR_NO_CACHE} \
        "${CTX}"
}

function _copy_tree() {
    # Copy a source tree into the build context, excluding VCS, virtualenvs,
    # build artifacts and caches so the context stays small and reproducible.
    local src="$1"
    local dst="$2"
    if command -v rsync >/dev/null 2>&1; then
        rsync -a \
            --exclude '.git' \
            --exclude '.venv' \
            --exclude 'venv' \
            --exclude 'dist' \
            --exclude 'build' \
            --exclude '*.egg-info' \
            --exclude '__pycache__' \
            --exclude '.pytest_cache' \
            --exclude '.mypy_cache' \
            "${src}/" "${dst}/"
    else
        # Fallback without rsync: copy then prune.
        mkdir -p "${dst}"
        cp -R "${src}/." "${dst}/"
        find "${dst}" -depth \
            \( -name '.git' -o -name '.venv' -o -name 'venv' -o -name 'dist' \
               -o -name 'build' -o -name '*.egg-info' -o -name '__pycache__' \
               -o -name '.pytest_cache' -o -name '.mypy_cache' \) \
            -exec rm -rf {} + 2>/dev/null || true
    fi
}

# Call the build_main() outline function
build_main "$@"
