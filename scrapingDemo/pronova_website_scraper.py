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

        # filters out duplicate links
        seen_urls = set()

        # if header:
        links = soup.find_all('a')

        for link in links:
            href = link.get('href')
            text = link.get_text(strip=True)

            if not href:
                continue

            if href.startswith('tel:'):
                phone_number = href.replace('tel:', '').strip()
                    
            elif href.startswith('mailto:'):
                email = href.replace('mailto:', '').strip()
                    
            elif href.startswith('http') or href.startswith('/'):
                full_url = urljoin(url, href)

                if not full_url.startswith("https://pronovapets.com/"):
                    continue   

                if full_url in seen_urls:
                    continue    # skip duplicates

                # add link to set
                seen_urls.add(full_url)

                try:
                    page = requests.get(full_url, headers=headers)
                    page_soup = BeautifulSoup(page.text, "html.parser")
                    soup_link = page_soup.title.string.strip() if page_soup.title else 'No Title'
                    page_content_div = page_soup.find('div', class_='page-content')
                    page_text = page_content_div.get_text(separator="\n", strip=True) if page_content_div else 'No .page-content found'

                    results.append({
                        'url': full_url,
                        'title': soup_link,
                        'content': page_text
                    })
                except Exception as e:
                    print(f"Failed to scrape {full_url}: {e}")
        
        return results
    else:
        return f"Failed to retrieve the webpage. Status code: {response.status_code}"


results = extract_text_from_url("https://pronovapets.com")

# create folder if it doesn't exist
os.makedirs("Pronova_files", exist_ok=True)

# define subfolder path inside Pronova_files
subfolder = os.path.join("Pronova_files", "scraped_pages")
os.makedirs(subfolder, exist_ok=True)  # create subfolder if it doesn't exist

# save each result as a separate .txt file inside the subfolder
for result in results:
    title = result.get('title', 'Untitled Page').strip()
    
    # clean filename: remove characters that are not allowed in file names
    safe_title = "".join(c for c in title if c.isalnum() or c in (" ", "_", "-")).rstrip()
    filename = safe_title[:100] + ".txt"  # limit filename length
    file_path = os.path.join(subfolder, filename)
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(result['content'])
        print(f"Saved file: {filename}")
    except Exception as e:
        print(f"Failed to save {filename}: {e}")