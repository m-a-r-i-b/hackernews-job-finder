import requests
from bs4 import BeautifulSoup

# Hacker news thread URL
def scrap_comments(url):
    response = requests.get(url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    comments = soup.find_all('tr', class_='athing comtr')
    
    comments_dict = {}
    commentCount = 0
    for comment in comments:
        indent = comment.find('td', class_='ind')
        if indent and indent.get('indent') == '0':
            commentText = comment.find('div', class_='commtext').get_text()
            if commentText:
                commentCount += 1
                comments_dict[commentCount] = {'text':commentText}

    print(f"Scraped {commentCount} top-level comments.")
    return comments_dict