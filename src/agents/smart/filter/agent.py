from agents.base.Agent import Agent
from agents.smart.filter.output import (
    FilterAgentOutput,
)
from const import AgentBrainModel
from agents.smart.filter.prompt.renderer import get_chat_prompt
from langfuse.decorators import langfuse_context, observe
from const import Step


class FilterAgent(Agent):
    def __init__(
        self,
        brain_model: AgentBrainModel = AgentBrainModel.GPT_3_5_Turbo_0125,
    ):
        prompt = get_chat_prompt()
        agent_output_class = FilterAgentOutput
        super().__init__(brain_model, prompt, agent_output_class)

    @observe()
    def run(
        self, user_msg: str, user_id: str, project_id: str, session_id: str
    ) -> FilterAgentOutput:
        langfuse_context.update_current_trace(
            user_id=user_id,
            name=project_id,
            session_id=session_id,
            tags=[Step.Filtering],
        )
        return super().run(user_msg)
