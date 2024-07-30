import pandas as pd
from ntscraper import Nitter
from flask import Flask, request, abort, render_template_string
import random
import requests
import re
import time
from fake_useragent import UserAgent

app = Flask(__name__)

# ----------- Set of rules to filter malicious requests ----------- 
rules = {
    'sql_injection': re.compile(r'(union|select|insert|delete|update|drop|alter).*', re.IGNORECASE),
    'xss_attack': re.compile(r'(<script>|<iframe>).*', re.IGNORECASE),
    'path_traversal': re.compile(r'(\.\./|\.\.).*', re.IGNORECASE)
}

# ----------- Middleware to check each request against WAF rules -----------
@app.before_request
def check_request_for_attacks():
    for attack_type, pattern in rules.items():
        if pattern.search(request.path) or pattern.search(request.query_string.decode()):
            abort(403, description=f'Request blocked by WAF: Detected {attack_type}')

@app.route('/')
def home():
    return 'Welcome to the safe web application guarded by our WAF!'

def get_random_proxy():
    proxies = [
        'http://proxy1:port',
        'http://proxy2:port',
        'http://proxy3:port'
    ]
    return random.choice(proxies)

def agent(username, mode, number):
    scraper = Nitter()
    ua = UserAgent()
    tweets = scraper.get_tweets(username, mode=mode, number=number)
    tweet_data = []

    for tweet in tweets['tweets']:
        random_ua = ua.random
        proxy = get_random_proxy()
        delay = random.uniform(1, 5)
        scraper.session = requests.Session()
        scraper.session.headers['User-Agent'] = random_ua
        scraper.session.proxies = {"http": proxy, "https": proxy}
        tweet_data.append({
            'tweet': tweet,
            'user_agent': random_ua,
            'agent': 'Nitter Scraper'  # Use string 'Nitter Scraper' to avoid recursion issues
        })
        time.sleep(delay)

    return tweet_data

@app.route('/tweets')
def scrape_tweets():
    print("Scrape Tweets route hit")  # Debug print
    tweet_data = agent('Web3Career', mode='user', number=5)
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Tweets</title>
        </head>
        <body>
            {% for data in tweet_data %}
                <p><strong>Tweet:</strong> {{ data.tweet }}</p>
                <p><strong>User Agent:</strong> {{ data.user_agent }}</p>
                <p><strong>Agent:</strong> {{ data.agent }}</p>
                <p>-------- Next Tweet --------</p>
            {% endfor %}
        </body>
        </html>
    ''', tweet_data=tweet_data)

# Start the web application on port 5000 with debug mode
if __name__ == '__main__':
    app.run(debug=True, port=5000)
