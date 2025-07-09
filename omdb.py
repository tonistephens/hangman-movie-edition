import requests
import random
import datetime
import re
import string
import time

API_KEY = '3c2a5e84'

def is_valid_title(title):
    # Check title has at least one letter, and is between 4 and 40 characters
    return re.search(r"[A-Za-z]", title) is not None and 4 <= len(title) <= 40

def get_random_query():
    # Generate random search string for querying API
    # 50% chance to return common fragment, otherwise random 2-4 letter sequence
    common_fragments = ['man', 'war', 'love', 'day', 'night', 'life', 'met']
    if random.random() < 0.5:
        return random.choice(common_fragments)
    return ''.join(random.choices(string.ascii_lowercase, k=random.randint(2, 4)))

def get_random_movie():
    base_url = "http://www.omdbapi.com/"
    # Try (up to) 6 attempts to get valid movie
    for attempt in range(6):
        query = get_random_query()  # Generate search term
        year = random.randint(1980, datetime.datetime.now().year)  # Random year from 1980 until now
        params = {
            'apikey': API_KEY,
            's': query,
            'type': 'movie',
            'y': year,
            'page': 1
        }

        try:
            # Make API request to search for movies
            resp = requests.get(base_url, params=params, timeout=3)
            if resp.ok:
                search_data = resp.json()
                if 'Search' in search_data:
                    # Shuffle search results to randomise selection
                    random.shuffle(search_data['Search'])
                    for movie in search_data['Search']:
                        title = movie.get('Title')
                        if title and is_valid_title(title):
                            # Get full details
                            detail_params = {
                                'apikey': API_KEY,
                                't': title
                            }
                            detail_resp = requests.get(base_url, params=detail_params)
                            if detail_resp.ok:
                                detail_data = detail_resp.json()
                                poster = detail_data.get('Poster')
                                # Return valid title and poster
                                if poster and poster != 'N/A':
                                    return title, poster
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
        time.sleep(1)

    # Fallback in case no movie found
    return "Hangman Default", None
