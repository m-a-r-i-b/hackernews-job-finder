import time

def meets_filter_criteria(thread_url, comment_id, db):
    time.sleep(0.2)
    db.update_threads_comment(thread_url, comment_id, {'filter': 'Done'})
    return True