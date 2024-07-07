import asyncio
import json
import random
import time
import queue
from steps.categorize import categorize
from steps.filter import meets_filter_criteria


def start_workers(num_workers, task_queue, websocket):
    from concurrent.futures import ThreadPoolExecutor
    executor = ThreadPoolExecutor(max_workers=num_workers)
    for _ in range(num_workers):
        executor.submit(worker, task_queue, websocket)


def worker(task_queue, websocket):
    while True:
        thread_url, comment_id,  db = task_queue.get()
        asyncio.run(process_comment(thread_url, comment_id, db, websocket))
        task_queue.task_done()


async def process_comment(thread_url, comment_id, db, websocket):
    if(await meets_filter_criteria(thread_url, comment_id, db, websocket)):
        pass
        # categorize(thread_url, comment_id, db)
        # extract_contact_info(thread_url, comment_id, db)
        # generate_cover_letter(thread_url, comment_id, db)
    return f"Comment {id} processed"

