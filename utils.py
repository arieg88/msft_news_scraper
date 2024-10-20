import time
import random
import ast
import os
import json

SP_TOP = ['Apple', 'Microsoft', 'Nvidia', 'Amazon', 'Meta', 'Alphabet', 'Berkshire Hathaway', 'Broadcom', 'Eli Lilly', 'Jpmorgan', 'Tesla'] 

def read_headers():
    with open('headers.txt', 'r') as file:
      headers = ast.literal_eval(file.read())

    with open('cookies.txt', 'r') as file:
      cookies = ast.literal_eval(file.read())
    return headers, cookies

def random_sleep(sleep_times=[2, 3, 4, 5, 6]):
    time.sleep(random.choice(sleep_times))

def get_new_headers_or_continue(url, next_data='month'):
    print(f'failed with {url}')
    inp = input(f'Enter 1 to Try agin, or Enter 2 to continue to the next {next_data}:\n')
    if inp == '1':
        return True
    elif inp == '2':
        return False
    else:
        print('Not valid input')
        return True
    
def save_articles(articles, company, month, year=2024):
    # Save the list of dictionaries to a JSON file after each update
    try:
        # Ensure the year directory exists
        os.makedirs(f'./articles/{company}/{year}', exist_ok=True)
        with open(f'./articles/{company}/{year}/{month}_articles.json', 'w') as json_file:
            json.dump(articles, json_file, indent=4)
        return True
    except:
        pass # sould raise some Couldntsave error
