from agents.base.Agent import Agent
from agents.keyword.output import (
    KeywordOutput,
)
from const import AgentBrainModel
from agents.keyword.prompt.renderer import get_chat_prompt


class KeywordAgent(Agent):
    def __init__(
        self,
        brain_model: AgentBrainModel = AgentBrainModel.GPT_3_5_Turbo_0125,
    ):
        prompt = get_chat_prompt()
        agent_output_class = KeywordOutput
        super().__init__(brain_model, prompt, agent_output_class)

    def run(
        self, user_msg: str
    ) -> KeywordOutput:
        return super().run(user_msg)
