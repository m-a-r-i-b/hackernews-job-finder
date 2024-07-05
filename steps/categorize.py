import time

def categorize(project_id, comment_id, db):
    time.sleep(0.2)
    db.update_comment(project_id, comment_id, {'categorize': 'Donee'})