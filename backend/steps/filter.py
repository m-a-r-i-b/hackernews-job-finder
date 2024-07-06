import json
import time

def meets_filter_criteria(thread_url, comment_id, db, frontend_websocket):
    time.sleep(0.2)

    socket_payload = {
        'thread_url': thread_url,
        'comment_id': comment_id,
        'payload': {
            'filter': 'Done'
        }
    }
    # Send the payload to the frontend
    try:
        print("trying to send data to FE")
        frontend_websocket.send_text(json.dumps(socket_payload))
    except Exception as e:
        print("Error sending data to frontend", e)

    db.update_threads_comment(thread_url, comment_id, {'filter': 'Done'})
    return True