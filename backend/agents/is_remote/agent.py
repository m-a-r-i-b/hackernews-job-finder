from agents.base.Agent import Agent
from agents.is_remote.output import (
    IsRemoteOutput,
)
from const import AgentBrainModel
from agents.is_remote.prompt.renderer import get_chat_prompt


class IsRemoteAgent(Agent):
    def __init__(
        self,
        brain_model: AgentBrainModel = AgentBrainModel.GPT_3_5_Turbo_0125,
    ):
        prompt = get_chat_prompt()
        agent_output_class = IsRemoteOutput
        super().__init__(brain_model, prompt, agent_output_class)

    def run(
        self, user_msg: str
    ) -> IsRemoteOutput:
        return super().run(user_msg)
