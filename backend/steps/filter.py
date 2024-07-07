import asyncio
import json
import random


async def meets_filter_criteria(thread_url, comment_id, db, websocket):
    # await asyncio.sleep(0.2)
    await asyncio.sleep(random.uniform(0, 0.2))

    socket_payload = {
        'thread_url': thread_url,
        'key': str(comment_id),
        'payload': {
            'filter': 'processing..'
        }
    }
    await push_update_to_frontend(socket_payload, websocket)

    await asyncio.sleep(random.uniform(0, 1))
    socket_payload = {
        'thread_url': thread_url,
        'key': str(comment_id),
        'payload': {
            'filter': 'OK'
        }
    }
    await push_update_to_frontend(socket_payload, websocket)


    db.update_threads_comment(thread_url, comment_id, {'filter': 'Done'})
    return True


async def push_update_to_frontend(socket_payload, websocket):
    try:
        await websocket['socket'].send_text(json.dumps(socket_payload))
    except Exception as e:
        print("Error sending data to frontend", e)
