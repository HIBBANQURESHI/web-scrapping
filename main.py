import pandas as pd
from ntscraper import Nitter

scraper = Nitter()

tweets = scraper.get_tweets('Web3Career', mode = 'user', number = 5)

for tweet in tweets ['tweets']:
    print(tweet)
    print('-------- Next Tweet --------')