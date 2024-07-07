import asyncio
import json
import random
import time
import queue
from steps.categorize import categorize
from steps.filter import meets_filter_criteria



async def send_to_frontend(socket_payload, websocket):
    try:
        await websocket['socket'].send_text(json.dumps(socket_payload))
    except Exception as e:
        print("Error sending data to frontend", e)

def worker(task_queue, websocket):
    while True:
        key = task_queue.get()
        time.sleep(random.uniform(0, 1))
        socket_payload = {
            'thread_url': "2",
            'key': str(key),
            'payload': {
                'filter': 'KK'
            }
        }
        print("trying to send data to FE")
        asyncio.run(send_to_frontend(socket_payload, websocket))
        task_queue.task_done()

def start_workers(num_workers, task_queue, websocket):
    from concurrent.futures import ThreadPoolExecutor
    executor = ThreadPoolExecutor(max_workers=num_workers)
    for _ in range(num_workers):
        executor.submit(worker, task_queue, websocket)


async def process_comment(thread_url, comment_id, db, frontend_websocket):
    if(await meets_filter_criteria(thread_url, comment_id, db, frontend_websocket)):
        pass
        # categorize(thread_url, comment_id, db)
        # extract_contact_info(thread_url, comment_id, db)
        # generate_cover_letter(thread_url, comment_id, db)
    return f"Comment {id} processed"

