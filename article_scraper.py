### TODO: Add code so that "load more" is pressed fully before beginning

import requests
from bs4 import BeautifulSoup
import json
import os

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def load_all_articles(topic_url):
    # set up selenium webdriver
    options = Options()
    options.binary_location = "/opt/google-chrome/chrome"

    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--incognito")

    driver = webdriver.Chrome(service=Service("/usr/local/bin/chromedriver"), options=options)
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    time.sleep(2)
    
    driver.get(topic_url)

    # click "Load More" until it's no longer present
    while True:
        try:
            # locate the "Load More" button and click it
            load_more_button = driver.find_element(By.CSS_SELECTOR, ".paging1-more a.button1")
            ActionChains(driver).move_to_element(load_more_button).click(load_more_button).perform()
            time.sleep(5)                               # wait for articles to load
        except:
            # break the loop if the "Load More" button is not found
            break
    
    # get page source after loading all articles
    page_content = driver.page_source
    driver.quit()

    return BeautifulSoup(page_content, 'html.parser')


def fetch_articles(soup, topic_name):
    articles_data = {}

    # find all articles under the topic
    articles = soup.find_all("article.card1")
    
    for article in articles:
        article_url = article.find('a')["href"]         # get the link to the article

        article_element = article.find("div.insert1 card1-main")
        
        title_element = article_element.find("h4") 
        title = title_element.text.strip()
        abbr_title = title.replace(" ", "-").lower()    # create an abbrieviated title for the article file

        # date_element = article_element.find("p.card1-date -t:11")
        # date = date_element.find("time")
        # publish_date = date.text.strip()                # extract date string
        # formatted_date = format_date(publish_date)      # convert date to MM-DD-YYYY

        date_element = article_element.find("time")
        publish_date = date_element.text.strip()        # extract date string
        formatted_date = format_date(publish_date)      # convert date to MM-DD-YYYY

        # fetch the content of the article
        article_content = fetch_article_content(article_url)

        # save the article content to a .txt file
        save_article_txt(abbr_title, article_content)

        # store article data in the dictionary
        articles_data[f"{abbr_title}.txt"] = {
            "source": article_url,
            "author": "American Animal Hospital Association",
            "topic": topic_name,
            "publishDate": formatted_date
        }

    return articles_data


def fetch_article_content(article_url):
    response = requests.get(article_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    content = soup.find('div', class_='wrap1-inner -restrain')
    
    return content.text.strip() if content else ""


def format_date(date_string):
    # convert date from e.g. "October 16, 2024" to "10-16-2024"
    month_day_year = date_string.split()
    month = month_day_year[0][:3]                       # first 3 letters of the month
    day = month_day_year[1].rstrip(',')                 # remove the comma
    year = month_day_year[2]

    month_mapping = {
        'jan': '1', 'feb': '2', 'mar': '3', 'apr': '4',
        'may': '5', 'jun': '6', 'jul': '7', 'aug': '8',
        'sep': '9', 'oct': '10', 'nov': '11', 'dec': '12'
    }

    return f"{month_mapping[month.lower()]}-{int(day):02d}-{year}"


def save_article_txt(filename, content):
    with open(f"{filename}", 'w') as file:
        file.write(content)


def main():
    topics = {
        "Behavior and Training": "https://www.aaha.org/for-pet-parents/?animals%5B%5D=86&topics%5B%5D=88",
        "Dental Care for Pet Parents": "https://www.aaha.org/for-pet-parents/?animals%5B%5D=86&topics%5B%5D=210",
        "Diabetes Management": "https://www.aaha.org/for-pet-parents/?animals%5B%5D=86&topics%5B%5D=94",
        # might not capture everything
        "Guidelines 101 for Pet Owners": "https://www.aaha.org/for-pet-parents/?animals%5B%5D=86&topics%5B%5D=92",
        "Nutrition": "https://www.aaha.org/for-pet-parents/?animals%5B%5D=86&topics%5B%5D=60",
        # might not capture everything
        "Preparing for Pet Ownership": "https://www.aaha.org/for-pet-parents/?animals%5B%5D=86&topics%5B%5D=91",
        "Preventive Health Care": "https://www.aaha.org/for-pet-parents/?animals%5B%5D=86&topics%5B%5D=334",
        # might not capture everything
        "Safety": "https://www.aaha.org/for-pet-parents/?animals%5B%5D=86&topics%5B%5D=66",
        "Senior Care": "https://www.aaha.org/for-pet-parents/?animals%5B%5D=86&topics%5B%5D=75",
        "Spay and Neuter": "https://www.aaha.org/for-pet-parents/?animals%5B%5D=86&topics%5B%5D=93",
        "Vaccinations": "https://www.aaha.org/for-pet-parents/?animals%5B%5D=86&topics%5B%5D=63",
        "What to Expect at the Vet": "https://www.aaha.org/for-pet-parents/?animals%5B%5D=86&topics%5B%5D=90"
    }

    all_articles = {}

    for topic, url in topics.items():
        soup = load_all_articles(url)
        articles_data = fetch_articles(url, topic)
        all_articles.update(articles_data)

    # save all articles data to a JSON file
    with open("articles_data.json", 'w') as json_file:
        json.dump(all_articles, json_file, ident=4)


if __name__ == "__main__":
    main()
