
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from os import environ

from nora_fleet.internals.graph.registry.agent_network import AgentNetwork


class MissingAgentCheck:
    """
    Convience and consolidation for checks against missing/misnamed agents.
    """

    @staticmethod
    def check_agent_network(agent_network: AgentNetwork, agent_name: str) -> AgentNetwork:
        """
        :param agent_network: The AgentNetwork to check
        :param agent_name: The name of the agent to use for the session.
        :return: The AgentNetwork corresponding to the agent_name
        """

        if agent_network is None:
            message = f"""
Agent named "{agent_name}" not found in manifest file: {environ.get("AGENT_MANIFEST_FILE")}.

Some things to check:
1. If the manifest file named above is None, know that the default points
   to the one provided with the nora-fleet library for a smoother out-of-box
   experience.  If the agent you wanted is not part of that standard distribution,
   you need to set the AGENT_MANIFEST_FILE environment variable to point to a
   manifest.hocon file associated with your own project(s).
2. Check that the environment variable AGENT_MANIFEST_FILE is pointing to
   the manifest.hocon file that you expect and has no typos.
3. Does your manifest.hocon file contain a key for the agent specified?
4. Does the value for the key in the manifest file have a value of 'true'?
5. Does your agent name have a typo either in the hocon file or on the command line?
"""
            raise ValueError(message)

        return agent_network
