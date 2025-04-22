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
        
        results = []

        # if header:
        links = soup.find_all('a')

        for link in links:
            href = link.get('href')
            text = link.get_text(strip=True)

            if not href:
                continue

            if href.startswith('tel:'):
                phone_number = href.replace('tel:', '').strip()
                # print(f"Found phone number: {phone_number}")
                    
            elif href.startswith('mailto:'):
                email = href.replace('mailto:', '').strip()
                    # print(f"Found email: {email}")
                    
            elif href.startswith('http') or href.startswith('/'):
                full_url = urljoin(url, href)
                    # print(f"Scraping: {text} -> {full_url}")

                try:
                    page = requests.get(full_url, headers=headers)
                    page_soup = BeautifulSoup(page.text, "html.parser")
                    soup_link = page_soup.title.string.strip() if page_soup.title else 'No Title'
                    page_text = page_soup.get_text(separator="\n", strip=True)

                    results.append({
                        'url': full_url,
                        'title': soup_link,
                        'content': page_text
                    })
                except Exception as e:
                    print(f"Failed to scrape {full_url}: {e}")
                    

        div_content = soup.find('div', class_='page-content')
        content = div_content.get_text() if div_content else 'Unknown'

        # scraping footer 
        div_footer = soup.find('div', class_="elementor elementor-134")
        footer = div_footer.get_text() if div_footer else 'Unknown'
        
        return content, results, footer
    else:
        return f"Failed to retrieve the webpage. Status code: {response.status_code}"

# def save_content(url):
#     content, results, footer = extract_text_from_url(url)

#     map_results = {}

#     os.makedirs('Pronova_files', exist_ok=True)

#     filepath = os.path.join(os.path.join('Pronova_files', 'home_page.txt'), 'w', encoding='utf-8') as file:
#     with open(filepath, 'w', encoding='utf-8') as file:
#         file.write(content)

#     map_results['home_page.txt'] = {
#         "link": url,
#         "title": "Home Page"
#     }

#     json_filename = 'pronova_files.json'
#     if os.path.exists(json_filename):
#         with open(json_filename, 'r+', encoding='utf-8') as json_file:
#             try:
#                 data = json.load(json_file)
#             except json.JSONDecodeError:
#                 data = {}
#             data[file_name] = entry
#             json_file.seek(0)
#             json.dump(data, json_file, indent=4)
#     else:
#         with open(json_filename, 'w', encoding='utf-8') as json_file:
#             json.dump({file_name: entry}, json_file, indent=4)


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

output = extract_text_from_url("https://pronovapets.com")
# extract_text_from_url("https://pronovapets.com/about-us/")
# save_content("https://pronovapets.com/the-kora-strip/")
# save_content("https://pronovapets.com/health-insights/")
# save_content("https://pronovapets.com/subscriptions/")
# save_content("https://pronovapets.com/contact-us/")
# save_content("https://pronovapets.com/veterinary-partners/")
# save_content("https://pronovapets.com/blog/")
# save_content("https://pronovapets.com/faqs/")
# save_content("https://pronovapets.com/waitlist/")

content, results, footer = output

data = {
    "main_content": content,
    "links": results,
    "footer": footer
}

# construct the path to the file
file_path = os.path.join("Pronova_files", "pronova_output.json")

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
