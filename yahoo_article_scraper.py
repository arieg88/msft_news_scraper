import ast
import requests
from bs4 import BeautifulSoup
import json 
from utils import *
import os

headers, cookies = read_headers()

def save_articles(articles, company, month):
    # Save the list of dictionaries to a JSON file after each update
    try:
        # Ensure the year directory exists
        os.makedirs(f'./articles/{company}/{year}', exist_ok=True)
        with open(f'./articles/{company}/{year}/{month}_articles.json', 'w') as json_file:
            json.dump(articles, json_file, indent=4)
        return True
    except:
        pass # sould raise some Couldntsave error

def scrape_yahoo_finance(urls, autosave=True):
    articles = []

    for url in urls:
        random_sleep([1,2])
        scraped = False
        while not scraped:
            try:
                response = requests.get(
                    url,
                    cookies=cookies,
                    headers=headers,
                )
            
                soup = BeautifulSoup(response.content, 'html.parser')
                title = soup.find('h1', class_='cover-title').text
                author = soup.find('div', class_='byline-attr-author').text
                date = soup.find('time').get('data-timestamp')
                text = ''
                for p in soup.find('div', class_='body').find_all('p'):
                    text += p.text
                    text += '\n'
                
                articles.append({'Date': date,
                                'Title': title,
                                'Author': author,
                                'Text': text})
                
                save_articles(articles, company, month)
                scraped = True
                print(f'Finished scraping article in {url}')

            except:
                new_headers = get_new_headers_or_continue(url, 'article')
                if new_headers:
                    headers, cookies = read_headers()
                else:
                    scraped = True

    return articles

year = 2024

for company in SP_TOP[2:4]:
    for month in range(1, 11):
        urls = {}
        # Load the list from a file using ast.literal_eval
        with open(f'./urls/{company}/{year}/{month}_urls.txt', 'r') as file:
            urls = ast.literal_eval(file.read())

        articles = scrape_yahoo_finance(urls)

        print(f'Finished scraping articles from Yahoo Finance in {month}/{year}')