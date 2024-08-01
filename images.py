import requests
from bs4 import BeautifulSoup
import os
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Function to download images
def download_image(url, file_name):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(file_name, 'wb') as file:
            file.write(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")

# Function to create a requests session with retry logic
def requests_session():
    session = requests.Session()
    retry = Retry(
        total=5,
        read=5,
        connect=5,
        backoff_factor=0.3,
        status_forcelist=(500, 502, 504)
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

# Function to scrape images from a specific Twitter account page
def scrape_images_from_twitter(username, count=10):
    url = f'https://twitter.com/{username}'
    session = requests_session()
    
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve the Twitter page for {username}: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    images = soup.find_all('img', {'src': lambda x: x and 'twimg.com/media' in x})

    if not os.path.exists('images'):
        os.makedirs('images')

    image_count = 0
    for image in images[:count]:
        image_url = image['src']
        if image_url.startswith('http'):
            file_name = f"images/{username}_{image_count}.jpg"
            download_image(image_url, file_name)
            image_count += 1
            print(f"Downloaded {file_name}")

# Scrape images from the Web3Career Twitter account
scrape_images_from_twitter('Web3Career', count=10)
