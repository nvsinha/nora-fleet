#!/bin/bash

# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

# Script that runs the docker file locally with proper mounts
# Usage: run.sh <CONTAINER_VERSION>
#

function check_directory() {
    working_dir=$(pwd)
    if [ "nora-fleet" == "$(basename "${working_dir}")" ]
    then
        # We are in the nora-fleet repo.
        # Change directories so that the rest of the script will work OK.
        cd nora_fleet || exit 1
    fi
}

function run() {

    check_directory

    CONTAINER_VERSION="${1:-0.0.1}"
    echo "Using CONTAINER_VERSION ${CONTAINER_VERSION}"
    echo "Using args '$*'"

    # Check for an environment file to pass to the docker run command.
    # This is optional, but if it is set and exists, we will use it.
    # Environment file should be a simple text file with lines of the form:
    #   VAR_NAME=VAR_VALUE
    # This allows us to pass in any collection of run-specific values
    env_file_cmd=""
    if [[ -n "${SERVICE_ENV_FILE:-}" && -f "$SERVICE_ENV_FILE" ]]; then
        echo "Using service environment file: $SERVICE_ENV_FILE"
        env_file_cmd="--env-file $(printf '%q' "$SERVICE_ENV_FILE")"
    elif [[ -z "${SERVICE_ENV_FILE:-}" ]]; then
        echo "SERVICE_ENV_FILE is not set."
    else
        echo "WARNING: '$SERVICE_ENV_FILE' does not exist."
    fi

    #
    # Host networking only works on Linux. Get the OS we are running on
    #
    OS=$(uname)
    echo "OS: ${OS}"

    # Using a default network of 'host' is actually easiest thing when
    # locally testing against a vault server container set up with https,
    # but allow this to be changeable by env var.
    network=${NETWORK:="host"}
    echo "Network is ${network}"

    SERVICE_NAME="NoraFleetAgents"
    # Assume the first port EXPOSEd in the Dockerfile is the input port
    DOCKERFILE=$(find . -name Dockerfile | sort | head -1)
    SERVICE_HTTP_PORT=$(grep ^EXPOSE < "${DOCKERFILE}" | head -1 | awk '{ print $2 }')
    echo "SERVICE_HTTP_PORT: ${SERVICE_HTTP_PORT}"

    # Note that we have to set the equivalent of the ulimit -n via the docker run
    # command line.  We don't want the ceiling of fds to interfere with how many
    # requests we can serve in the container.
    FILE_DESCRIPTOR_MAX=100000

    # Run the docker container in interactive mode
    #   Mount the 1st command line arg as the place where input files come from
    #   Slurp in the rest as environment variables, all of which are optional.

    docker_cmd="docker run --rm -it \
        --ulimit nofile=${FILE_DESCRIPTOR_MAX}:${FILE_DESCRIPTOR_MAX} \
        --name=$SERVICE_NAME \
        --network=$network \
        -e OPENAI_API_KEY \
        -e ANTHROPIC_API_KEY \
        -e AGENT_SESSION_REQUIRE_HTTPS=false \
        -e NORA_LOG_SENSITIVE=true \
        ${env_file_cmd} \
        -p $SERVICE_HTTP_PORT:$SERVICE_HTTP_PORT \
            nora-fleet/nora-fleet:$CONTAINER_VERSION"

    if [ "${OS}" == "Darwin" ];then
        # Host networking does not work for non-Linux operating systems
        # Remove it from the docker command
        docker_cmd=${docker_cmd/--network=$network/}
    fi

    echo "${docker_cmd}"
    $docker_cmd
}

function main() {
    run "$@"
}

# Pass all command line args to function
main "$@"
