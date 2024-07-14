import json
import queue
import time
from fastapi import FastAPI, File, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from agents.resume_parser.agent import ResumeParserAgent
from utils import construct_socket_message, notify_frontend, read_docx, read_pdf
from models import CommentRead, Criteria, Experience, ThreadDetails
from persistence.fake_database import Database
from scraper import scrap_comments
from worker import start_workers
from dotenv import load_dotenv
load_dotenv(".env")


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
frontend_websocket = {} # Has to be an object to be able to pass by reference
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



@app.post("/submit-thread/")
async def submit_item(thread: ThreadDetails):
    comments_dict = scrap_comments(thread.url)
    db.create_thread(thread.title, thread.url, comments_dict)
    
    for comment_id in comments_dict.keys():
        task_queue.put((thread.url, comment_id, comments_dict[comment_id]['text'], db))
  
    return {"title": thread.title, "url": thread.url}

@app.get("/get-threads/")
async def get_threads():
    threads = db.get_all_threads()
    return [{'url': url, 'title': data['title'], 'comment_count': len(data['comments'])} for url, data in threads.items()]

@app.get("/get-thread-by-url/")
async def get_thread(url: str):
    return db.get_thread_by_url(url)

@app.post("/update-comment-read-status/")
async def update_comment_read_status(comment_details: CommentRead):
    db.update_threads_comment(comment_details.thread_url, comment_details.comment_id, {'is_read': comment_details.is_read})
    await notify_frontend(construct_socket_message(
        thread_url=comment_details.thread_url,
        comment_id=comment_details.comment_id,
        step='is_read',
        info=comment_details.is_read
    ), frontend_websocket)



@app.post("/upload-resume/")
async def upload_file(file: UploadFile = File(...)):
    content = ""
    if file.content_type == "application/pdf":
        content = await read_pdf(file)
    elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" or file.content_type == "application/msword":
        content = await read_docx(file)
    else:
        return {"error": "Unsupported file type"}
    
    try:
        resume_details = json.loads(ResumeParserAgent(db).run(content).json())['resume_details']
    except Exception as e:
        print("Error parsing resume", e)
        resume_details = content

    return {"filename": file.filename, "content": resume_details}


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


