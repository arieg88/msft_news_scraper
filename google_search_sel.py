import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from utils import *  # Assuming read_headers is defined in utils
import os

# Set up Chrome options for headless browsing (optional)
chrome_options = Options()
# chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize the WebDriver
# service = Service('path/to/chromedriver')  # Provide the path to your ChromeDriver
driver = webdriver.Chrome(options=chrome_options)

# Read headers and cookies
headers, cookies = read_headers()

# site_url = 'https://finance.yahoo.com/'
site_url = 'https://www.ft.com/'

def get_urls(soup, ext=''):
    urls = []
    for link in soup.find_all('a'):
        try:
            url = link.get('href')  # Get the href attribute safely
            if url and site_url in url:
                # url = href[href.find(site_url):href.find(ext) + len(ext)]
                # if url != '' and url != 'http':
                urls.append(url)
        except Exception as e:
            print(f"Error parsing link: {e}")
    return urls

# Define search queries

def get_queries(company, site, year):
    queries = [(f"intitle:{company}+site:{site}+after:{year:04d}/{month:02d}/01+before:{year:04d}/{month+1:02d}/01", month) for month in range(1, 12)]
    queries.append((f"intitle:{company}+site:{site}+after:{year:04d}/12/01+before:{(year+1):04d}/01/01", 12))
    return queries


def get_monthly_dict(queries, company, year, site_name):
    monthly_dict = {}
    for query, month in queries:
        print(f'Searching for month: {month}')
        url = 'https://www.google.com/search?q=' + query
        urls = []
        start = 0
        urls_len= 0

        while True:
            if start > 0:
                url = f'https://www.google.com/search?q={query}&start={start}'

            # Open the URL with Selenium
            driver.get(url)
            # if x:
            #     time.sleep(60)
            #     x = False
            random_sleep()

            # Get the page source and parse it with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Check if soup is valid
            if soup is None:
                print("Failed to parse the page.")
                print(driver.page_source)  # Print the raw HTML for debugging
                break
            
            urls += get_urls(soup)


            
            # If no URLs found, check for new headers or continue to the next month
            if urls_len == len(urls):  
                all_ul = soup.find_all('ul')
                if len(all_ul[1].find_all('li')) == 4:
                    print(f'Done with {month} (moving to next month)')
                    break
                
                if get_new_headers_or_continue(url):
                    headers, cookies = read_headers()
                    continue
                else:
                    print(f'Done with {month} (moving to next month)')
                    break
            # Check if we have reached the end of the results
            urls_len = len(urls)

            start += 10  # Move to the next page

        monthly_dict[month] = urls

        # Ensure the year directory exists
        os.makedirs(f'./urls/{company}/{site_name}/{year}', exist_ok=True)
        # Save results for the month
        with open(f'./urls/{company}/{site_name}/{year}/{month}_urls.txt', 'w') as file:
            file.write(str(urls))

    return monthly_dict

year = 2024
site = 'www.ft.com'
for company in SP_TOP:
    queries = get_queries(company, site, 2024)
    monthly_dict = get_monthly_dict(queries, company, year, 'ft')

# Close the WebDriver
driver.quit()