import queue
from fastapi import WebSocket


task_queue = queue.Queue()
frontend_websocket: WebSocket = None