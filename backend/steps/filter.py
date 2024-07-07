import asyncio
import json
import time
from fastapi import WebSocket


async def meets_filter_criteria(thread_url, comment_id, db, frontend_websocket: WebSocket):
    # time.sleep(0.2)
    await asyncio.sleep(0.2)
    socket_payload = {
        'thread_url': thread_url,
        'key': str(comment_id),
        'payload': {
            'filter': 'KK'
        }
    }
    # Send the payload to the frontend
    try:
        print("trying to send data to FE")
        await frontend_websocket.send_text(json.dumps(socket_payload))
    except Exception as e:
        print("Error sending data to frontend", e)

    db.update_threads_comment(thread_url, comment_id, {'filter': 'Done'})
    return True