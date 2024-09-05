# case-in-context
Case in Context bot, a tool that identifies which case an article is talking about.

Often, wire services like the AP and other news media do a bad job of linking to court opinions and dockets when they write stories about the law. This is a bot that attempts to remedy that, by targeting tweets posted by the AP and identifying the relevant case using ChatGPT and Courtlistener. You can use another LLM if you prefer; just make sure to adjust the code accordingly.

## Installation

### 1. Clone the repository

First, clone the project repository from GitHub and install the dependencies:

```bash
git clone https://github.com/v-anne/case-in-context.git
cd case-in-context
pip install -r requirements.txt
```

### 2. Modify the .env file with your API keys for Twitter/X, OpenAI, and CourtListener.

### 3. Run the python script. It will find the latest tweets from the AP that match and identify the case(s) discussed by each article.
