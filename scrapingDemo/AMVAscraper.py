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

        # Example selectors for AVMA website - adjust these after inspecting the site
        topic_h1 = soup.find('h1')  # Adjust based on AVMA's article title element
        topic = topic_h1.get_text().strip() if topic_h1 else 'Unknown'

        paragraphs = soup.find_all('p')  # This should capture all main content paragraphs
        text = '\n'.join([para.get_text() for para in paragraphs])

        # Placeholder for author (adjust if author info is available)
        author = 'Unknown'

        # Example date selector - adjust based on AVMA's date element
        date_element = soup.find('time')  # Use the correct tag/attribute if date is elsewhere
        date = date_element.get_text().strip() if date_element else 'Unknown'

        return topic, author, date, text
    else:
        return f"Failed to retrieve the webpage. Status code: {response.status_code}"


def save_content_to_files(url):
    result = extract_text_from_url(url)
    if isinstance(result, str):  # error message
        return
 
    topic, author, date, text = result
    
    
    # Create a filename based on the topic
    filename = f"{topic.replace('?', '').replace(':', '').replace(',', '').replace(' ', '_').replace('!', '').lstrip('_')}.txt"
    print(filename)
        
    # Ensure the directory exists
    os.makedirs('ScrapedFiles_2', exist_ok=True)
    
    # Save the text content to a txt file in the ScrapedFiles folder
    filepath = os.path.join('ScrapedFiles_2', filename)
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
    json_filename = 'sources_1.json'
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
        divs = soup.find_all('div', class_="field field--name-body field--type-text-with-summary field--label-hidden clearfix text-formatted avma__component--body-copy field__item")#class_='field--name-body field--type-text-with-summary field--label-hidden clearfix text-formatted avma__component--body-copy field__item')

        hrefs = []
        for div in divs:
            links = div.find_all('a', href=True)  # Find all <a> tags with href attribute
            for link in links:
                if link['href'].startswith('/resources'):  # Only include links that start with /resources, some bad links exist
                    url = "https://www.avma.org" + link['href'] 
                    hrefs.append(url)
                
        return hrefs
    else:
        return f"Failed to retrieve the webpage. Status code: {response.status_code}"

# Main URL for AVMA pet care articles
urls = extract_hrefs_from_divs("https://www.avma.org/resources-tools/pet-owners/petcare")


for url in urls[:-1]: #drop the last url because it forwards to another page, not an article
    save_content_to_files(url)

## also, it looks like ' apostraphe is replaced with \u2019 in sources_json
## i went in and fixed this, but can edit the code to do automatically later