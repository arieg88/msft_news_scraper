import ast
import requests
from bs4 import BeautifulSoup
import json 
from utils import *
import os
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

headers, cookies = read_headers()


# Open the desired URL
url = 'https://www.cnn.com/cnn-underscored/reviews/best-scanner-apps'
# driver.get(url)

response = requests.get(url, headers=headers, cookies=cookies)

random_sleep([1,2,3])

# Get the page source and parse it with BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Check if soup is valid
if soup is None:
    print("Failed to parse the page.")
    print(response.content)  # Print the raw HTML for debugging
else:
    header = soup.find('h1', class_='headline__text inline-placeholder vossi-headline-text').text
    author =soup.find('span', class_='byline__name').text
    date = soup.find('div', class_='timestamp vossi-timestamp').text
    article = soup.find('div', class_='article__content-container').text
    print(header)
    print(author)
    print(date)
    print(article)