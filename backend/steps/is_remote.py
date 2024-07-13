import asyncio
import json
import random
from agents.is_remote.agent import IsRemoteAgent
from agents.is_remote.output import IsRemoteOutput
from const import Step
from utils import construct_socket_message, notify_frontend_of_processing_status, notify_frontend

async def is_remote(thread_url, comment_id, comment_text, db, websocket):
    try:
        step = Step.IS_REMOTE_WORK_ALLOWED
        notify_frontend_of_processing_status(thread_url, comment_id, step, websocket)

        output: IsRemoteOutput = IsRemoteAgent().run(comment_text)
        print("Output = ",output)

        notify_frontend(construct_socket_message(thread_url,comment_id,step, output), websocket)
        db.update_threads_comment(thread_url, comment_id, {Step.IS_REMOTE_WORK_ALLOWED: output})
        return True
    except Exception as e:
            print(f"Error processing comment {comment_id}", e)


