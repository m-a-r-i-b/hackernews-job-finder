import time

def meets_filter_criteria(project_id, comment_id, db):
    time.sleep(0.2)
    db.update_comment(project_id, comment_id, {'filter': 'Done'})
    return True