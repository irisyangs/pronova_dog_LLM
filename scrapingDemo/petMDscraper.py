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

        #topic
        topic_h1 = soup.find('h1', class_='article_title_article_title__98_zt')
        topic = topic_h1.get_text() if topic_h1 else 'Unknown'

        #main content
        paragraphs = soup.find_all('p')
        text = '\n'.join([para.get_text() for para in paragraphs])

        #author
        try:
            author_div = soup.find('div', class_='author_little_little_author_content__eXAgS')
            author = author_div.find('a').get_text() if author_div else 'Unknown'
        except AttributeError:
            author = 'PetMD Editorial' 

        #date
        date_span = soup.find('span', class_='author_little_nowrap__8UQcE')
        date = date_span.get_text() if date_span else 'Unknown'

        return topic, author, date, text
    else:
        return f"Failed to retrieve the webpage. Status code: {response.status_code}"


def save_content_to_files(url):
    topic, author, date, text = extract_text_from_url(url)
    
    # Create a filename based on the topic
    topic = topic.replace('/', '_')
    filename = f"{topic.replace('?', '').replace(':', '').replace(',', '').replace(' ', '_').replace('!','').lstrip('_')}.txt"


    
    # Ensure the directory exists
    os.makedirs('ScrapedFiles', exist_ok=True)
    
    # Save the text content to a txt file in the ScrapedFiles folder
    filepath = os.path.join('ScrapedFiles', filename)
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(text)
    
    # Prepare the entry for the JSON file
    entry = {
        "Topic": topic,
        "URL": url,
        "Author": author,
        "Date": date
    }
    
    # Append the entry to the JSON file
    json_filename = 'sources.json'
    if os.path.exists(json_filename):
        with open(json_filename, 'r+', encoding='utf-8') as json_file:
            try:
                data = json.load(json_file)
            except json.JSONDecodeError:
                data = {}
            data[filename] = entry
            json_file.seek(0)
            json.dump(data, json_file, indent=4)
    else:
        with open(json_filename, 'w', encoding='utf-8') as json_file:
            json.dump({filename: entry}, json_file, indent=4)


def extract_hrefs_from_divs(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        divs = soup.find_all('div', class_='kib-grid__item kib-grid__item--span-4@min-xs kib-grid__item--span-4@md kib-grid__item--span-4@min-lg az_list_grid_item__KWCvL')
        hrefs = [div.find('a')['href'] for div in divs if div.find('a')]
        return hrefs
    else:
        return f"Failed to retrieve the webpage. Status code: {response.status_code}"

urls = extract_hrefs_from_divs("https://www.petmd.com/dog/conditions")

for url in urls:
    save_content_to_files("https://www.petmd.com/" + url)