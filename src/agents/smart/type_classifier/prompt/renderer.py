import os
from agents.base.AgentOutput import AgentObservation
from const.smart_contracts import SmartContractType
from langchain_core.prompts import (
    ChatPromptTemplate,
)
from const.index import (
    FORMAT_INSTRUCTIONS_PLACEHOLDER,
)
from const.mappings import Step
from memory.blackboard.Blackboard import BlackBoard
from utils.index import assemble_chat_prompt_template, render_template


def _get_sys_prompt_template() -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    context = {
        "smart_contract_types": SmartContractType,
        "observation_step_completed": AgentObservation.STEP_COMPLETED,
        "observation_take_user_input": AgentObservation.TAKE_USER_INPUT,
        "observation_types": AgentObservation,
        "format_instructions_placeholder": FORMAT_INSTRUCTIONS_PLACEHOLDER,
    }
    return render_template(current_dir, context, "template.j2")


def get_chat_prompt(blackboard: BlackBoard) -> ChatPromptTemplate:
    sys_template = ("system", _get_sys_prompt_template())
    return assemble_chat_prompt_template(
        sys_template, blackboard, Step.Type_Classification
    )
