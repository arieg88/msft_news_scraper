import ast
import requests
from bs4 import BeautifulSoup
import json 
from utils import *
import os

headers, cookies = read_headers()

def scrape_cnn(urls, autosave=True):
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

                # Get the page source and parse it with BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')

                # Check if soup is valid
                if soup is None:
                    print("Failed to parse the page.")
                    print(response.content)  # Print the raw HTML for debugging
                else:
                    title = soup.find('span', class_='headline__text').text
                    author =soup.find('a', class_='n-content-tag--author').text
                    date = soup.find('time').text
                    text = soup.find('article', id='article-body').text
 
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

for company in SP_TOP:
    for month in range(1, 11):
        urls = {}
        # Load the list from a file using ast.literal_eval
        with open(f'./urls/{company}/{year}/{month}_urls.txt', 'r') as file:
            urls = ast.literal_eval(file.read())

        articles = scrape_cnn(urls)

        print(f'Finished scraping articles from Yahoo Finance in {month}/{year}')