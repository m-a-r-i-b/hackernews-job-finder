from agents.base.Agent import SmartAgent
from agents.smart_contract_developer.output import SmartContractDeveloperOutput
from const.models import AgentBrainModel
from agents.smart_contract_developer.prompt.renderer import get_chat_prompt
from memory.blackboard.Blackboard import BlackBoard
from const.mappings import Step
from langfuse.decorators import langfuse_context, observe


class SmartContractDeveloperAgent(SmartAgent):
    def __init__(
        self,
        blackboard: BlackBoard,
        brain_type: AgentBrainModel = AgentBrainModel.GPT_3_5_Turbo_0125,
    ):
        self.blackboard = blackboard
        prompt = get_chat_prompt(blackboard)
        agent_output_class = SmartContractDeveloperOutput
        super().__init__(brain_type, prompt, agent_output_class, blackboard)

    @observe()
    def run(
        self, user_msg: str, user_id: str, project_id: str, session_id: str
    ) -> SmartContractDeveloperOutput:
        langfuse_context.update_current_trace(
            user_id=user_id,
            name=project_id,
            session_id=session_id,
            tags=[Step.Smartcontract_Development],
        )
        return super().run(user_msg)
