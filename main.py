import requests
from bs4 import BeautifulSoup

req = requests.get('https://x.com/search?q=jobs&src=typed_query')

# Parse the HTML content
soup = BeautifulSoup(req.content, "html.parser")

spans = soup.find_all('span', class_='css-1jxf684')

for span in spans:
    text = span.get_text(strip=True)
    print(text)
