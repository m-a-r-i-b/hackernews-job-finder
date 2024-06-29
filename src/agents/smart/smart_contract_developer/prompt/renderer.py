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
from agents.smart_contract_developer.prompt.specific_instructions.index import (
    SMART_CONTRACT_TYPE_SPECIFIC_INSTRUCTIONS,
)
from utils.index import assemble_chat_prompt_template, render_template


def _get_smart_contract_type_specific_instructions(
    smart_contract_type: SmartContractType,
) -> str:
    return SMART_CONTRACT_TYPE_SPECIFIC_INSTRUCTIONS.get(smart_contract_type, "")


def _get_sys_prompt_template(blackboard: BlackBoard) -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))

    user_messages_in_previous_steps = blackboard.get_user_msg_history(
        blackboard.get_completed_steps()
    )

    chosen_smart_contract_type = blackboard.get_information(Step.Type_Classification)[
        "smart_contract_type"
    ]

    smart_contract_type_specific_instructions = (
        _get_smart_contract_type_specific_instructions(chosen_smart_contract_type)
    )

    context = {
        "user_messages_in_previous_steps": user_messages_in_previous_steps,
        "chosen_smart_contract_type": chosen_smart_contract_type,
        "smart_contract_type_specific_instructions": smart_contract_type_specific_instructions,
        "format_instructions_placeholder": FORMAT_INSTRUCTIONS_PLACEHOLDER,
        "observation_step_completed": AgentObservation.STEP_COMPLETED,
        "observation_take_user_input": AgentObservation.TAKE_USER_INPUT,
    }
    return render_template(current_dir, context, "template.j2")


def get_chat_prompt(blackboard: BlackBoard) -> ChatPromptTemplate:
    sys_template = ("system", _get_sys_prompt_template(blackboard))
    return assemble_chat_prompt_template(
        sys_template, blackboard, Step.Smartcontract_Development
    )
