import asyncio
import concurrent.futures
import json
import random
import time
from fastapi import WebSocket
from steps.categorize import categorize
from steps.filter import meets_filter_criteria
from globals import task_queue


def start_workers(num_workers):
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=num_workers)
    for _ in range(num_workers):
        executor.submit(worker)


def worker():
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
        try:
            print("trying to send data to FE")
            global frontend_websocket
            asyncio.run(frontend_websocket.send_text(json.dumps(socket_payload)))
            
        except Exception as e:
            print("Error sending data to frontend", e)
        
        task_queue.task_done()
        
# def process_comments_in_background(comments_dict: dict, thread_url: str, db, frontend_websocket):
#     with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
#         for comment_id in comments_dict.keys():
#             executor.submit(process_comment, thread_url, comment_id, db, frontend_websocket)


def process_comments_in_background(thread_url, comments_dict, db, frontend_websocket, loop):

    for comment_id in comments_dict.keys():
        asyncio.run_coroutine_threadsafe(process_comment(thread_url, comment_id, db, frontend_websocket), loop)


    # for comment_id in comments_dict.keys():
    #     await process_comment(thread_url, comment_id, db, frontend_websocket)
    #     # tasks.append(task)
        # tasks.append(process_comment(thread_url, comment_id, db, frontend_websocket))
    # await asyncio.gather(*tasks)


async def process_comment(thread_url, comment_id, db, frontend_websocket):
    if(await meets_filter_criteria(thread_url, comment_id, db, frontend_websocket)):
        pass
        # categorize(thread_url, comment_id, db)
        # extract_contact_info(thread_url, comment_id, db)
        # generate_cover_letter(thread_url, comment_id, db)
    return f"Comment {id} processed"

