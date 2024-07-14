from agents.base.Agent import Agent
from agents.cover_letter.output import (
    CoverLetterOutput,
)
from const import AgentBrainModel
from agents.cover_letter.prompt.renderer import get_chat_prompt


class CoverLetterAgent(Agent):
    def __init__(
        self,
        db,
        brain_model: AgentBrainModel = AgentBrainModel.GPT_4_Omni,
    ):  
        self.my_experience = db.get_experience()
        prompt = get_chat_prompt(self.my_experience)
        agent_output_class = CoverLetterOutput
        super().__init__(brain_model, prompt, agent_output_class)

    def run(
        self, user_msg: str
    ) -> CoverLetterOutput:
        if not self.my_experience or self.my_experience == "":
            return CoverLetterOutput(cover_letter='-')
        return super().run(user_msg)
