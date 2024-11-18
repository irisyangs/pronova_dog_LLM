import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os
import time

def extract_text_from_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    # response = requests.get(url, headers=headers)
    response = requests.get(url, headers=headers, timeout=10)  # timeout in seconds

    time.sleep(3)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        #topic
        topic_h1 = soup.find('h1', class_='article_title_article_title__98_zt')
        topic = topic_h1.get_text() if topic_h1 else 'Unknown'

        #main content
        paragraphs = soup.find_all('p')
        text = '\n'.join([para.get_text() for para in paragraphs])

        word_count = len(text.split())
        if word_count < 100:
            print(f"Error: The content has fewer than 100 words in {url}.")
            return None, None, None, None

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

    print(filename, author, date)
    # return

    # Ensure the directory exists
    os.makedirs('ScrapedFiles_petMD_behavior', exist_ok=True)
    
    # Save the text content to a txt file in the ScrapedFiles folder
    filepath = os.path.join('ScrapedFiles_petMD_behavior', filename)
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
    json_filename = 'sources_petMD_behavior.json'
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
        # divs = soup.find_all('div', class_='kib-grid__item kib-grid__item--span-4@min-xs kib-grid__item--span-4@md kib-grid__item--span-4@min-lg az_list_grid_item__KWCvL')
        divs = soup.find_all('div', class_='article_card_articleCard__UmssU')
        hrefs = [div.find('a')['href'] for div in divs if div.find('a')]
        hrefs = [href for href in hrefs if href != '/dog/behavior/why-do-dogs-bring-you-toys-when-you-get-home']
        # bad link i found
        return hrefs
    else:
        return f"Failed to retrieve the webpage. Status code: {response.status_code}"


# page 2

urls = extract_hrefs_from_divs("https://www.petmd.com/dog/behavior")
# urls = extract_hrefs_from_divs("https://www.petmd.com/dog/behavior/p/2")



for url in urls:
    # print(url)
    save_content_to_files("https://www.petmd.com" + url)

# same bug with ' --> \u2019

# How_to_Teach_a_Dog_to_Come_to_You_in_Any_Environment.txt

# /dog/training/obedience-training-dogs-4-easy-cues-master