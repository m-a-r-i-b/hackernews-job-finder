import requests
from bs4 import BeautifulSoup
import os

from constants import RAW_COMMENTS_DIR

def scrappingComments(url):
    response = requests.get(url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    comments = soup.find_all('tr', class_='athing comtr')
    
    if not os.path.exists(RAW_COMMENTS_DIR):
        os.makedirs(RAW_COMMENTS_DIR)

    commentCount = 0
    for comment in comments:
        indent = comment.find('td', class_='ind')
        if indent and indent.get('indent') == '0':
            commentText = comment.find('div', class_='commtext').get_text()
            if commentText:
                commentCount += 1
                with open(f'{RAW_COMMENTS_DIR}/comment_{commentCount}.txt', 'w', encoding='utf-8') as f:
                    f.write(commentText)
    
    print(f"Saved {commentCount} top-level comments.")

url = 'https://news.ycombinator.com/item?id=40563283'
scrappingComments(url)