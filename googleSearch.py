import pandas as pd
import requests
import re
import os
from dotenv import load_dotenv

load_dotenv()



def main(query, result_total=10):
    """
    Main function to orchestrate the process of querying the Google Search API.

    : param query: Search term
    : param result_total: Total number of results to retrieve
    """
    items = []
    reminder = result_total % 10
    if reminder > 0:
        pages = result_total // 10 + 1
    else:
        pages = result_total // 10

    for i in range(0, pages):
        if pages == i + 1 and reminder > 0:
            payload = build_payload(query, start= (i+1) * 10, num=reminder)
        else:
            payload = build_payload(query, start= (i+1) * 10)
        response = make_request(payload)
        items += response['items']

    # Create results directory
    if not os.path.exists('results'):
        os.makedirs('results')

    query_string_clean = clean_filename(query)
    df = pd.json_normalize(items)
    df.to_excel('Google Search Result_{0}.xlsx'.format(query_string_clean), index=False)


def clean_filename(filename):
    """
    Clean the filename by removing special characters.

    : param filename: The filename to clean
    : return: The cleaned filename
    """
    filename = re.sub('[^A-Za-z0-9]+', '', filename) #remove special characters
    return filename[:100] #truncate filename to 100 characters

def build_payload(query, start=1, num=10, date_restrict='d1', **params):
    """
    Build the payload for the Google Search API request.

    : param query: Search term
    : param start: First result to retrieve
    : param num: Number of results to retrieve
    :param search_type: Type of search to perform (default is undefined, 'IMAGE' for image search)
    :param link_site: Search within a specified site (e.g. 'https://www.google.com')
    : param date_restrict: Restrict results to last modification date
    : param params: Aditional parameters to pass to the request

    : return: Dictionary containing the API request payload
    """
    payload = {
        'q': query,
        'start': start,
        'num': num,
        'dateRestrict': date_restrict,
        'key': api_key, 
        'cx': search_engine_id,  
    }
    payload.update(params)
    return payload

def make_request(payload):
    """
    Function to send the GET request to the Google Search API and handle potential errors.

    : param payload: Dictionary containing the API request payload
    : return: JSON response from the API
    """
    response = requests.get(url, params=payload)
    if response.status_code != 200:
        raise Exception(f'Google Search API request failed with status {response.status_code}, {response.text}')
    return response.json()

if __name__ == '__main__':
    api_key = os.getenv("CUSTOM_GOOGLE_SEARCH_API_KEY")
    search_engine_id = os.getenv("SEARCH_ENGINE_ID")
    search_query = 'ukraine war'
    total_results = 35

    url = 'https://www.googleapis.com/customsearch/v1'
    
    main(search_query, total_results)

