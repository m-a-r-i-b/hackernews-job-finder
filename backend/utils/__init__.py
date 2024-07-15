import asyncio
import json
import random
from models import SocketMessage
from const import USER_MSG_KEY, Step
from langchain_core.prompts import ChatPromptTemplate
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from PyPDF2 import PdfReader
from docx import Document
import io
from fastapi import UploadFile



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



def construct_socket_message(thread_url, comment_id, step, info) -> SocketMessage:
    return {
        'thread_url': thread_url,
        'comment_id': str(comment_id),
        step: info,
    }


async def notify_frontend_of_processing_status(thread_url, comment_id, step, websocket):
    socket_payload: SocketMessage = construct_socket_message(thread_url, comment_id, step, 'PROCESSING')
    await notify_frontend(socket_payload, websocket)


async def notify_frontend(msg_obj: SocketMessage, websocket):
    try:
        await asyncio.sleep(random.uniform(0, 1))
        await websocket['socket'].send_text(json.dumps(msg_obj))
    except Exception as e:
        print("Error sending data to frontend", e)



async def read_pdf(file: UploadFile):
    pdf_reader = PdfReader(io.BytesIO(await file.read()))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


async def read_docx(file: UploadFile):
    docx_reader = Document(io.BytesIO(await file.read()))
    text = ""
    for para in docx_reader.paragraphs:
        text += para.text + "\n"
    return text