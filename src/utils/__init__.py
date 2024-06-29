from const import USER_MSG_KEY
from langchain_core.prompts import ChatPromptTemplate
from jinja2 import Environment, FileSystemLoader, StrictUndefined


def render_template(curr_dir, context, template_name) -> str:
    env = Environment(
        loader=FileSystemLoader(["./common/prompt_partials", curr_dir]),
        undefined=StrictUndefined,
    )
    raw_template = env.get_template(template_name)
    return raw_template.render(context)



def assemble_chat_prompt_template(sys_template):
    msg_list = [sys_template, ("human", "{" + USER_MSG_KEY + "}")]
    return ChatPromptTemplate.from_messages(msg_list)