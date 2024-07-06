import concurrent.futures
from steps.categorize import categorize
from steps.filter import meets_filter_criteria



def process_comments_in_background(comments_dict: dict, thread_url: str, db, frontend_websocket):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for comment_id in comments_dict.keys():
            executor.submit(process_comment, thread_url, comment_id, db, frontend_websocket)


def process_comment(thread_url, comment_id, db, frontend_websocket):
    if(meets_filter_criteria(thread_url, comment_id, db, frontend_websocket)):
        categorize(thread_url, comment_id, db, frontend_websocket)
        # extract_contact_info(thread_url, comment_id, db)
        # generate_cover_letter(thread_url, comment_id, db)
    return f"Comment {id} processed"

