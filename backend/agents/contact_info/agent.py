from agents.base.Agent import Agent
from agents.contact_info.output import (
    ContactInfoOutput,
)
from const import AgentBrainModel
from agents.contact_info.prompt.renderer import get_chat_prompt


class ContactInfoAgent(Agent):
    def __init__(
        self,
        db,
        brain_model: AgentBrainModel = AgentBrainModel.GPT_3_5_Turbo_0125,
    ):
        prompt = get_chat_prompt()
        agent_output_class = ContactInfoOutput
        super().__init__(brain_model, prompt, agent_output_class)

    def run(
        self, user_msg: str
    ) -> ContactInfoOutput:
        return super().run(user_msg)
