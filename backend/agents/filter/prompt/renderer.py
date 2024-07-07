import os
from langchain_core.prompts import (
    ChatPromptTemplate,
)
from const import FORMAT_INSTRUCTIONS_PLACEHOLDER
from utils import assemble_chat_prompt_template, render_template


def _get_sys_prompt_template() -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    context = {
        "format_instructions_placeholder": FORMAT_INSTRUCTIONS_PLACEHOLDER,
        "criteria": """
        Mandatory Criteria:
        1. Provides remote work
        Optional Criteria:
        1. Is related to GenAI , Generative AI, or LLMs
        2. Is related to NestJS, React, or Python
        """,
    }
    return render_template(current_dir, context, "template.j2")


def get_chat_prompt() -> ChatPromptTemplate:
    sys_template = ("system", _get_sys_prompt_template())
    return assemble_chat_prompt_template(sys_template)
