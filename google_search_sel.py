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

def get_urls(soup):
    urls = []
    for link in soup.find_all('a'):
        try:
            href = link.get('href')  # Get the href attribute safely
            if href and 'https://finance.yahoo.com/' in href:
                url = href[href.find('https://finance.yahoo.com/'):href.find('.html') + 5]
                if url != '' and url != 'http':
                    urls.append(url)
        except Exception as e:
            print(f"Error parsing link: {e}")
    return urls

# Define search queries
year = 2023
queries = [(f"intitle:microsoft+site:finance.yahoo.com+after:{year:04d}/{month:02d}/01+before:{year:04d}/{month+1:02d}/01", month) for month in range(1, 12)]
queries.append((f"intitle:microsoft+site:finance.yahoo.com+after:{year:04d}/12/01+before:{(year+1):04d}/01/01", 12))

monthly_dict = {}
# x = True
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
    os.makedirs(f'./urls/{year}', exist_ok=True)
    # Save results for the month
    with open(f'./urls/{year}/{month}_urls.txt', 'w') as file:
        file.write(str(urls))

# Close the WebDriver
driver.quit()