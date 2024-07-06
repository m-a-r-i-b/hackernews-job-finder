from fastapi import FastAPI, BackgroundTasks
from models import Criteria, Experience, ThreadDetails
from persistence.fake_database import Database
from scraper import scrap_comments
from worker import process_comments_in_background

app = FastAPI()
db = Database()


@app.post("/submit-thread/")
async def submit_item(thread: ThreadDetails, background_tasks: BackgroundTasks):
    if not db.get_experience():
        return {"status": "error", "msg": "Experience not set."}
    
    if not db.get_criteria():
        return {"status": "error", "msg": "Criteria not set."}
    
    comments_dict = scrap_comments(thread.url)
    db.create_thread(thread.url, comments_dict)
    background_tasks.add_task(process_comments_in_background, comments_dict, thread.url, db)

    return {"title": thread.title, "url": thread.url}


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