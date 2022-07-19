

# scraper.py
import requests
from bs4 import BeautifulSoup

url = 'https://yamakasiwear.ru/collection/izvestnye-lichnosti?page=2'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
quotes = soup.find_all('div', class_='empty-catalog-message')
print(quotes)
1