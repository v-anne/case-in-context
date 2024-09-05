import requests
import os

BEARER_TOKEN = os.getenv("BEARER_TOKEN")

twitter_url = "https://api.twitter.com/2/tweets/search/recent"
twitter_query_params = {
    'query': 'from:AP "federal court" OR "appeals court"'
}

twitter_headers = {
    "Authorization": f"Bearer {BEARER_TOKEN}"
}

response = requests.get(twitter_url, headers=twitter_headers, params=twitter_query_params)
