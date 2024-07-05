import requests
from bs4 import BeautifulSoup
import concurrent.futures
import time
from persistence.fake_database import Database
from steps.categorize import categorize
from steps.filter import meets_filter_criteria


def scrappingComments(url):
    response = requests.get(url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    comments = soup.find_all('tr', class_='athing comtr')
    
    response = {}
    commentCount = 0
    for comment in comments:
        indent = comment.find('td', class_='ind')
        if indent and indent.get('indent') == '0':
            commentText = comment.find('div', class_='commtext').get_text()
            if commentText:
                commentCount += 1
                response[commentCount] = {'text':commentText}
    
    print(f"Saved {commentCount} top-level comments.")
    return response


def process_item(project_id, comment_id, db):

    if(meets_filter_criteria(project_id, comment_id, db)):
        categorize(project_id, comment_id, db)
        # extract_contact_info(project_id, comment_id, db)
        # generate_cover_letter(project_id, comment_id, db)

    return f"Item {id} processed"



url = 'https://news.ycombinator.com/item?id=40563283'
comments_dict = scrappingComments(url)

db = Database()
db.create_project(url,comments_dict)

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # As long as there are items to process
    while comments_dict:
        # Pick the next item
        id, text = comments_dict.popitem()
        # Submit the item to be processed by the pool
        future = executor.submit(process_item, url, id, db)