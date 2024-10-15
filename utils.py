import time
import random
import ast

def read_headers():
    with open('headers.txt', 'r') as file:
      headers = ast.literal_eval(file.read())

    with open('cookies.txt', 'r') as file:
      cookies = ast.literal_eval(file.read())
    return headers, cookies

def random_sleep(sleep_times=[2, 3, 4, 5, 6]):
    time.sleep(random.choice(sleep_times))
2
def get_new_headers_or_continue(url, next_data='month'):
    print(f'failed with {url}')
    inp = input('change headers files and press 1 or continue to the next {next_data} by pressing 2:\n')
    if inp == '1':
        return True
    elif inp == '2':
        return False
    else:
        print('Not valid input')
        return True