import asyncio
from concurrent.futures import ThreadPoolExecutor
import json
import queue
import random
import threading
import time
from fastapi import FastAPI, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from models import Criteria, Experience, ThreadDetails
from persistence.fake_database import Database
from scraper import scrap_comments
from worker import start_workers
from typing import List



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)
db = Database()
task_queue = queue.Queue()
frontend_websocket = {}

start_workers(5, task_queue, frontend_websocket)

@app.websocket("/socket-endpoint")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    frontend_websocket['socket'] = websocket  # Add websocket to the list
    try:
        while True:
            data = await websocket.receive_text()
            time.sleep(1)
    except WebSocketDisconnect:
        print("Socket disconnected..")
        pass


@app.get("/test-post-socket/")
async def test_socket():
    socket_payload = {
        'thread_url': "1",
        'key': "2",
        'payload': {
            'filter': 'F',
            "categorize": "C"
        }
    }

    try:
        print("trying to send data to FE")
        await frontend_websocket.send_text(json.dumps(socket_payload))
    except Exception as e:
        print("Error sending data to frontend", e)

    

@app.post("/submit-thread/")
async def submit_item(thread: ThreadDetails,  background_tasks: BackgroundTasks):
    if not db.get_experience():
        return {"status": "error", "msg": "Experience not set."}
    
    if not db.get_criteria():
        return {"status": "error", "msg": "Criteria not set."}
    
    comments_dict = scrap_comments(thread.url)
    db.create_thread(thread.title, thread.url, comments_dict)
    
    for comment_id in comments_dict.keys():
        task_queue.put(comment_id)
    # loop = asyncio.get_event_loop()
    # background_tasks.add_task(run_in_thread, process_comments_in_background, thread.url, comments_dict, db, frontend_websocket, loop)
   
    # asyncio.create_task(process_comments_in_background(comments_dict, thread.url, db, frontend_websocket))
    # process_comments_in_background(comments_dict, thread.url, db, frontend_websocket)

    return {"title": thread.title, "url": thread.url}

@app.get("/get-threads/")
async def get_threads():
    threads = db.get_all_threads()
    return [{'url': url, 'title': data['title'], 'comment_count': len(data['comments'])} for url, data in threads.items()]

@app.get("/get-thread-by-url/")
async def get_thread(url: str):
    return db.get_thread_by_url(url)


@app.post("/submit-experience/")
async def submit_item(exp: Experience):
    db.set_experience(exp.experience)

@app.get("/get-experience/")
async def get_experience():
    return db.get_experience()


@app.post("/submit-criteria/")
async def submit_item(criteria: Criteria):
    db.set_criteria(criteria)

@app.get("/get-criteria/")
async def get_criteria():
    return db.get_criteria()


# uvicorn server:app --reload