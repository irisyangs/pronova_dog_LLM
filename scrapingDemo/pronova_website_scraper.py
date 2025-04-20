import requests
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from urllib.parse import urljoin
import json
import os

def extract_text_from_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # header
        header = soup.find('header') or soup.find('nav', class_='wpr-mobile-nav-menu-container')

        if header:
            header_links = header.find_all('a')

            for link in header_links:
                href = link.get('href')
                text = link.get_text(strip=True)

                if href:
                    div_content = soup.find('div', class_='page-content')
                    content = div_content.get_text() if div_content else 'Unknown'

                    if href.startswith('tel:'):
                        phone_number = href.replace('tel:', '').strip()
                        print(f"Found phone number: {phone_number}")
                    
                    elif href.startswith('mailto:'):
                        email = href.replace('mailto:', '').strip()
                        print(f"Found email: {email}")
                    
                    elif href.startswith('http') or href.startswith('/'):
                        full_url = urljoin(url, href)
                        print(f"Scraping: {text} -> {full_url}")

                        try:
                            page = requests.get(full_url, headers=headers)
                            page_soup = BeautifulSoup(page.text, "html.parser")
                            soup_link = page_soup.title.string if page_soup.title else 'No Title'
                            print(f"Page Title: {soup_link}")
                        except Exception as e:
                            print(f"Failed to scrape {full_url}: {e}")
                    
                    else:
                        print(f"Skipping non-web link: {href}")
        
        # main page content
        div_content = soup.find('div', class_='page-content')
        content = div_content.get_text() if div_content else 'Unknown'

        # scraping footer 
        div_footer = soup.find('div', class_="elementor elementor-134")
        footer = div_footer.get_text() if div_footer else 'Unknown'
        
        return content, soup_link, footer
    else:
        return f"Failed to retrieve the webpage. Status code: {response.status_code}"

def save_content(url):
    content, link, footer = extract_text_from_url(url)

    print(link)

    file_name = link

    os.makedirs('Pronova_files', exist_ok=True)

    filepath = os.path.join('Pronova_files', file_name)
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)

    entry = {
        "Link": link
    }

    json_filename = 'pronova_files.json'
    if os.path.exists(json_filename):
        with open(json_filename, 'r+', encoding='utf-8') as json_file:
            try:
                data = json.load(json_file)
            except json.JSONDecodeError:
                data = {}
            data[file_name] = entry
            json_file.seek(0)
            json.dump(data, json_file, indent=4)
    else:
        with open(json_filename, 'w', encoding='utf-8') as json_file:
            json.dump({file_name: entry}, json_file, indent=4)


# def extract_hrefs_from_divs(url):
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
#     }
#     response = requests.get(url, headers=headers)
    
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')
#         # divs = soup.find_all('div', class_='kib-grid__item kib-grid__item--span-4@min-xs kib-grid__item--span-4@md kib-grid__item--span-4@min-lg az_list_grid_item__KWCvL')
#         divs = soup.find_all('div', class_='article_card_articleCard__UmssU')
#         hrefs = [div.find('a')['href'] for div in divs if div.find('a')]
#         return hrefs
#     else:
#         return f"Failed to retrieve the webpage. Status code: {response.status_code}"


save_content("https://pronovapets.com")
# save_content("https://pronovapets.com/about-us/")
# save_content("https://pronovapets.com/the-kora-strip/")
# save_content("https://pronovapets.com/health-insights/")
# save_content("https://pronovapets.com/subscriptions/")
# save_content("https://pronovapets.com/contact-us/")
# save_content("https://pronovapets.com/veterinary-partners/")
# save_content("https://pronovapets.com/blog/")
# save_content("https://pronovapets.com/faqs/")
# save_content("https://pronovapets.com/waitlist/")



    