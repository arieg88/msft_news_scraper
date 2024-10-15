import requests
from bs4 import BeautifulSoup
import urllib.parse
import time
import random
import ast
from utils import *

headers, cookies = read_headers()
def get_urls(soup):
  urls = []
  # Find all divs with the class 'BVG0Nb

  for link in soup.find_all('a'):
    try:
      if 'https://finance.yahoo.com/' in link.get('href'):
        url = link['href']
        url = url[url.find('https://finance.yahoo.com/'):url.find('.html')+5]
        if url != '' and url != 'http':
          urls.append(url)
    except:
      pass
  return urls


def get_next_page_url(soup):
  # Find the <a> tag with aria-label="Next page"
  next_page = soup.find_all('div')
  print(next_page)
  next_page_url = 'https://www.google.com' + next_page

  return next_page_url

sleep_times = [2, 3, 4, 5, 6]

read_headers()

# queries = [(f"intitle:microsoft+site:finance.yahoo.com+after:2024/{month:02d}/01+before:2024/{month+1:02d}/01", month) for month in range(1,11)]
queries = [(f"intitle:microsoft+site:finance.yahoo.com+after:2024/{month:02d}/01+before:2024/{month+1:02d}/01", month) for month in range(10,11)]
monthly_dict = {}
for query, month in queries:
  print(month)
  url = 'https://www.google.com/search?q=' + query
  urls = []
  start = 0
  while True:
    urls_len = len(urls)
    print(urls_len)
    if start > 0:
      url = 'https://www.google.com/search?q=' + query + f'&start={start}'
    start += 10
    random_sleep()
    response = requests.get(
      url,
      cookies=cookies,
      headers=headers,
    )
    try:
      soup = BeautifulSoup(response.content, 'html.parser')
      if soup == None:
        print(response.content)
        break
      urls += get_urls(soup)

      if url is None or urls_len == len(urls):
        get_new_headers = get_new_headers_or_continue(url)
        if get_new_headers:
          headers, cookies = read_headers()
        else:
          print(f'done with {month}')
          break
    except:
      pass

      

  monthly_dict[month] = urls

  with open(f'{month}_urls.txt', 'w') as file:
    file.write(str(urls))

with open('all_urls_dict.txt', 'w') as file:
    file.write(str(monthly_dict))