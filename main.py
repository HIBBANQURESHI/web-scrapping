import pandas as pd
from ntscraper import Nitter
import requests
import random

def agent(username, mode, number):
    scraper = Nitter()

    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/8'
    ]

    tweets = scraper.get_tweets(username, mode=mode, number=number)

    for tweet in tweets['tweets']:
        random_ua = random.choice(user_agents)

        scraper.session = requests.Session()
        scraper.session.headers['User-Agent'] = random_ua

        print(tweet)
        print('-------- Next Tweet --------')
        print(agent)
        print(user_agents)

tweets = agent('Web3Career', mode='user', number=5)
