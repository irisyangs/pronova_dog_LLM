import requests
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
import json
import os

def extract_text_from_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # main page content
        div_content = soup.find('div', class_='page-content')
        content = div_content.get_text() if div_content else 'Unknown'

        # link
        containers_with_links = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "div"])
        links = [container.a['href'] for container in containers_with_links if container.a]

        # scraping links
        for link in links:
            response = requests.get(link, headers=headers)
            soup_link = BeautifulSoup(response.text, 'html.parser')

        # scraping footer 

        div_footer = soup.find('div', class_= "elementor elementor-134")
        footer = div_footer.get_text() if div_footer else 'Unknown'
        
        return content, soup_link, footer
    else: 
        return f"Failed to retrieve the webpage. Status code: {response.status_code}"

# def save_content(url):
#     content, link, footer = extract_text_from_url(url)

#     file_name = 

#     os.makedirs('Pronova_files', exist_ok=True)

#     filepath = os.path.join('Pronova_files', )
#     with open(filepath, 'w', encoding='utf-8') as file:
#         file.write(content)

def save_content_to_files(url):
    topic, author, date, text = extract_text_from_url(url)
    
    # Create a filename based on the topic
    topic = topic.replace('/', '_')
    filename = f"{topic.replace('?', '').replace(':', '').replace(',', '').replace(' ', '_').replace('!','').lstrip('_')}.txt"

    print(filename, author, date)
    # return

    # Ensure the directory exists
    os.makedirs('ScrapedFiles_petMD_nutrition', exist_ok=True)
    
    # Save the text content to a txt file in the ScrapedFiles folder
    filepath = os.path.join('ScrapedFiles_petMD_nutrition', filename)
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
    json_filename = 'sources_petMD_nutrition.json'
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
        return hrefs
    else:
        return f"Failed to retrieve the webpage. Status code: {response.status_code}"
            



print(extract_text_from_url("https://pronovapets.com"))



    