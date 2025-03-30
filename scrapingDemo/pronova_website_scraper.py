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

def save_content():
    return None



            



extract_text_from_url("pronovapets.com")



    