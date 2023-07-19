
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

url = 'https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/krakow/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
prices_per_sqm = []
while True:
    page_link_el = soup.select('a[data-testid="pagination-forward"]')
    if not page_link_el:
        break
    price_elements = soup.select('span.css-643j0o')
    for price_element in price_elements:
        price_text = price_element.text
        price_per_sqm = float(price_text.split('-')[-1].replace('zł/m²', '').strip())
        prices_per_sqm.append(price_per_sqm)
    
    link_el = page_link_el[0]
    link = urljoin(url, link_el.get('href'))
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'lxml')

if prices_per_sqm:
    average_price_per_sqm = sum(prices_per_sqm) / len(prices_per_sqm)
    print(f"Average price per m²: {average_price_per_sqm:.2f} zł/m²")
else:
    print("No price data found.")