from agents.base.Agent import Agent
from agents.smart.filter.output import (
    FilterAgentOutput,
)
from const import AgentBrainModel
from agents.smart.filter.prompt.renderer import get_chat_prompt
from const import Step


class FilterAgent(Agent):
    def __init__(
        self,
        brain_model: AgentBrainModel = AgentBrainModel.GPT_3_5_Turbo_0125,
    ):
        prompt = get_chat_prompt()
        agent_output_class = FilterAgentOutput
        # super().__init__(brain_model, prompt, agent_output_class)

    def run(
        self, user_msg: str, user_id: str, project_id: str, session_id: str
    ) -> FilterAgentOutput:
        return super().run(user_msg)
