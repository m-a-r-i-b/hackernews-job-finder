from agents.base.Agent import Agent
from agents.resume_parser.output import (
    ResumeParserOutput,
)
from const import AgentBrainModel
from agents.resume_parser.prompt.renderer import get_chat_prompt


class ResumeParserAgent(Agent):
    def __init__(
        self,
        db,
        brain_model: AgentBrainModel = AgentBrainModel.GPT_4_Omni,
    ):
        prompt = get_chat_prompt()
        agent_output_class = ResumeParserOutput
        super().__init__(brain_model, prompt, agent_output_class)

    def run(
        self, user_msg: str
    ) -> ResumeParserOutput:
        return super().run(user_msg)
