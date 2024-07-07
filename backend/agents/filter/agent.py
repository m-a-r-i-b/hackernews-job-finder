from agents.base.Agent import Agent
from agents.filter.output import (
    FilterAgentOutput,
)
from const import AgentBrainModel
from agents.filter.prompt.renderer import get_chat_prompt


class FilterAgent(Agent):
    def __init__(
        self,
        brain_model: AgentBrainModel = AgentBrainModel.GPT_3_5_Turbo_0125,
    ):
        prompt = get_chat_prompt()
        agent_output_class = FilterAgentOutput
        super().__init__(brain_model, prompt, agent_output_class)

    def run(
        self, user_msg: str
    ) -> FilterAgentOutput:
        return super().run(user_msg)
