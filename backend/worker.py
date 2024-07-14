import asyncio
import json
from agents import STEP_TO_AGENT_MAPPING
from utils import construct_socket_message, notify_frontend_of_processing_status, notify_frontend
from const import EXECUTION_PLAN, Step


def start_workers(num_workers, task_queue, websocket):
    from concurrent.futures import ThreadPoolExecutor
    executor = ThreadPoolExecutor(max_workers=num_workers)
    for _ in range(num_workers):
        executor.submit(worker, task_queue, websocket)


def worker(task_queue, websocket):
    while True:
        thread_url, comment_id, comment_text,  db = task_queue.get()
        try:
            asyncio.run(process_comment(thread_url, comment_id, comment_text, db, websocket))
        except Exception as e:
            print(f"-- Failed to process comment: {comment_id}", e)
            # TODO Maybe push update to FE to unhide processing status
        task_queue.task_done()


async def process_comment(thread_url, comment_id, comment_text, db, websocket):

    for step in EXECUTION_PLAN:
        try:
            await notify_frontend_of_processing_status(thread_url, comment_id, step, websocket)
            agent_for_step = STEP_TO_AGENT_MAPPING[step]
            output = json.loads(agent_for_step(db).run(comment_text).json())

            await notify_frontend(construct_socket_message(thread_url,comment_id, step, output), websocket)
            db.update_threads_comment(thread_url, comment_id, {step: output})

            if step == Step.IS_REMOTE_WORK_ALLOWED and (not output['allows_remote_work']):
                return # No need to process remaining steps if remote work is not allowed
        except Exception as e:
                print(f"Error processing comment {comment_id}", e)
        
    return f"Comment {id} processed"

