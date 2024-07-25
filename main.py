import requests
from bs4 import BeautifulSoup

req = requests.get('https://codesignservices.com/contact')

soup = BeautifulSoup(req.content, "html.parser")

name_field = soup.find('input', {'name': 'hibban'})
email_field = soup.find('input', {'name': 'hibban@gmail.com'})
message_field = soup.find('textarea', {'name': 'scrapper'})

name = name_field.get('value', 'No name field found') if name_field else 'No name field found'
email = email_field.get('value', 'No email field found') if email_field else 'No email field found'
message = message_field.get_text(strip=True) if message_field else 'No message field found'

print(f'Name: {name}')  
print(f'Email: {email}')
print(f'Message: {message}')
