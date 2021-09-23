import requests
from bs4 import BeautifulSoup
import pandas as pd

baseurl = "https://www.zara.com/es/es/search?searchTerm=camiseta%20blanca&section=MAN"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
productlinks = []
t = {}
data = []
c = 0
# for x in range(1,2):

k = requests.get(
    'https://www.thewhiskyexchange.com/c/35/japanese-whisky?pg={}&psize=24&sort=pasc'.format(x)).text
soup = BeautifulSoup(k, 'html.parser')
productlist = soup.find_all(
    "li", {"class": "product-grid-product _product product-grid-product--SEARCH-columns product-grid-product--0th-column"})
# tambe hi ha de la segona columna

for product in productlist:
    link = product.find("a", {"class": "product-card"}).get('href')
    productlinks.append(baseurl + link)

i = 0
for link in productlinks:

    f = requests.get(link, headers=headers).text
    hun = BeautifulSoup(f, 'html.parser')

# aquí es fan proves per trobar més info del producte.
    try:
        price = hun.find(
            "p", {"class": "product-action__price"}).text.replace('\n', "")
    except:
        price = None

    try:
        image_url = hun.find(
            'div', {"class": "product-main__image-container"}).img['src']
    except:
        image_url = None

    whisky = {"price": price, "product_url": image_url,
              "prodcutlinks": productlinks[i]}
    data.append(whisky)
    i = i+1
    # print(whisky)

df = pd.DataFrame(data)
print(df)

# df.to_csv('Whiskeys.csv', index=False)
