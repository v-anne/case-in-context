import requests
import os
from openai import OpenAI


BEARER_TOKEN = os.getenv("BEARER_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
COURTLISTENER_API_KEY = os.getenv("COURTLISTENER_API_KEY")


twitter_url = "https://api.twitter.com/2/tweets/search/recent"
twitter_query_params = {
    'query': 'from:AP "federal court" OR "appeals court"'
}

twitter_headers = {
    "Authorization": f"Bearer {BEARER_TOKEN}"
}

response = requests.get(twitter_url, headers=twitter_headers, params=twitter_query_params)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Failed to fetch data: {response.status_code}")

# LLM function call
client = OpenAI()

response = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {
      "role": "system",
      "content": "You will be provided with a news article, and then have to extract certain information in JSON format. Return a JSON with the following structure: {Judge: "", Date: "", Court: ""}. Court should be abbreviated using this courtlistener page: https://www.courtlistener.com/help/api/jurisdictions/ e.g., ca5, flmd, etc."
    },
    {
      "role": "user",
      "content": "AP_article_text"
    }
  ],
  temperature=0.5,
  max_tokens=64,
  top_p=1
)

result = response.choices[0].message

courtlistener_url = "https://www.courtlistener.com/q"
courtlistener_query_params = {
    'q': "",
    'court_id': result["Court"],
    'assigned_to_id': result["Judge"],
    'type': 'r'
}

courtlistener_headers = {
    'Authorization': f'Token {COURTLISTENER_API_KEY}'
}

response = requests.get(courtlistener_url, headers=courtlistener_headers, params=courtlistener_query_params)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Failed to fetch data: {response.status_code}")