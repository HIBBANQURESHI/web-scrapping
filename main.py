import requests
from bs4 import BeautifulSoup

req = requests.get('https://webscraper.io/test-sites/e-commerce/allinone')

soup = BeautifulSoup(req.content, "html.parser")

products = soup.find_all('div', class_='thumbnail')

for product in products:

    name = product.find('a', class_='title').get_text(strip=True)
    
    price = product.find('h4', class_='price').get_text(strip=True)
    
    description = product.find('p', class_='description')
    description = description.get_text(strip=True) if description else 'No description available'

    print(f'Name: {name}')
    print(f'Price: {price}')
    print(f'Description: {description}')
    print('---')
