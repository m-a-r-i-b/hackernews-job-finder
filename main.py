import requests
from bs4 import BeautifulSoup
import concurrent.futures
import time
from persistence.fake_database import Database


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
                response[commentCount] = commentText
    
    print(f"Saved {commentCount} top-level comments.")
    return response


def process_item(item, value):
    for _ in range(3):
        print(f"Processing item {item}"+('.'*_))
        time.sleep(0.2)  
    return f"Item {item} processed"




def worker_pool(items_dict):
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # As long as there are items to process
        while items_dict:
            # Pick the next item
            key, value = items_dict.popitem()
            # Submit the item to be processed by the pool
            future = executor.submit(process_item, key, value)
            results.append(future)
    
    # Wait for all results to be processed
    # for future in concurrent.futures.as_completed(results):
    #     print(future.result())

    print("yoo=======================================")

url = 'https://news.ycombinator.com/item?id=40563283'
res = scrappingComments(url)

db = Database()
db.create_project(url,res)