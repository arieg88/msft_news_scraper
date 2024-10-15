import ast
import requests
from bs4 import BeautifulSoup
import json 
from utils import *

headers, cookies = read_headers()

urls = {}
# for month in range(1,10):
for month in [8,9,10]:
    # Load the list from a file using ast.literal_eval
    with open(f'{month}_urls.txt', 'r') as file:
        urls = ast.literal_eval(file.read())

    articles = []

    for url in urls:
        random_sleep([1,2,3])
        response = requests.get(
            url,
            cookies=cookies,
            headers=headers,
        )
        try:
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

            # Save the list of dictionaries to a JSON file after each update
            with open(f'{month}_articles.json', 'w') as json_file:
                json.dump(articles, json_file, indent=4)

            print(f'Finished with {url}')
        except:
            new_headers = get_new_headers_or_continue(url)
            if new_headers:
                headers, cookies = read_headers()
            else:
                pass

