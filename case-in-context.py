import os
import json
import requests
from openai import OpenAI


BEARER_TOKEN = os.getenv("BEARER_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
COURTLISTENER_API_KEY = os.getenv("COURTLISTENER_API_KEY")


twitter_query_url = "https://api.twitter.com/2/tweets/search/recent"
twitter_query_params = {
    'query': 'from:AP "federal court" OR "appeals court"'
}

twitter_query_headers = {
    "Authorization": f"Bearer {BEARER_TOKEN}"
}

response = requests.get(twitter_query_url, headers=twitter_query_headers, params=twitter_query_params)

tweet_id = response["tweet_id"]

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

twitter_post_url = "https://api.twitter.com/2/tweets"
twitter_post_headers = {
    'Authorization': f"Oauth {BEARER_TOKEN}",
    'Content-type': 'application/json'
}

twitter_post_data = {
    "reply": {
        "in_reply_to_tweet_id": f"{tweet_id}"
    },
    "text": f"Here is the case this article is likely discussing: \n courtlistener.com/{response[0]["absolute_url"]}"
}

response = requests.post(twitter_post_url, headers=twitter_post_headers, data=json.dumps(twitter_post_data))

if response.status_code == 201:
    print("Tweet posted successfully.")
else:
    print(f"Failed to post tweet: {response.status_code}")
    print(response.text)