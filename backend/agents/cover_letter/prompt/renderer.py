import os
from langchain_core.prompts import (
    ChatPromptTemplate,
)
from const import FORMAT_INSTRUCTIONS_PLACEHOLDER
from utils import assemble_chat_prompt_template, render_template


def _get_sys_prompt_template(my_experience: str) -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    context = {
        "format_instructions_placeholder": FORMAT_INSTRUCTIONS_PLACEHOLDER,
        "my_experience": my_experience
    }
    return render_template(current_dir, context, "template.j2")


def get_chat_prompt(my_experience: str) -> ChatPromptTemplate:
    sys_template = ("system", _get_sys_prompt_template(my_experience))
    return assemble_chat_prompt_template(sys_template)
