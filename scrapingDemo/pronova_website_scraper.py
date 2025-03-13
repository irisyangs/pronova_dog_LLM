import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os

def extract_text_from_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # topic
        topic_h1 = soup.find('h1', class_='entry-title')
        topic = topic_h1.get_text() if topic_h1 else 'Unknown'

        div_content = soup.find('div', class_='content')
        content = div_content.get_text() if div_content else 'Unknown'

        #author
        try:
            author_div = soup.find('div', class_='author_little_little_author_content__eXAgS')
            author = author_div.find('a').get_text() if author_div else 'Unknown'

        



    