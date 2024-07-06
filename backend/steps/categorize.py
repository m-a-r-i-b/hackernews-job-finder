import time

def categorize(thread_url, comment_id, db):
    time.sleep(0.2)
    db.update_threads_comment(thread_url, comment_id, {'categorize': 'Donee'})