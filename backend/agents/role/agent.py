from agents.base.Agent import Agent
from agents.role.output import (
    RoleOutput,
)
from const import AgentBrainModel
from agents.role.prompt.renderer import get_chat_prompt


class RoleAgent(Agent):
    def __init__(
        self,
        brain_model: AgentBrainModel = AgentBrainModel.GPT_3_5_Turbo_0125,
    ):
        prompt = get_chat_prompt()
        agent_output_class = RoleOutput
        super().__init__(brain_model, prompt, agent_output_class)

    def run(
        self, user_msg: str
    ) -> RoleOutput:
        return super().run(user_msg)
