from agents.base.Agent import Agent
from agents.test.output import (
    TestOutput,
)
from const import AgentBrainModel
from agents.test.prompt.renderer import get_chat_prompt


class TestAgent(Agent):
    def __init__(
        self,
        brain_model: AgentBrainModel = AgentBrainModel.GPT_3_5_Turbo_0125,
    ):
        prompt = get_chat_prompt()
        agent_output_class = TestOutput
        super().__init__(brain_model, prompt, agent_output_class)

    def run(
        self, user_msg: str
    ) -> TestOutput:
        return super().run(user_msg)
