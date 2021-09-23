from bs4 import BeautifulSoup
import requests
import json
import lxml
import sys

headers = {  # <-- so the Google will treat your script as a "real" user browser.
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

response = requests.get(
  'https://www.zara.com/es/es/search?searchTerm=camisa%20blanca&section=MAN',
  headers=headers).text

soup = BeautifulSoup(response, 'lxml')


data = []

original_stdout = sys.stdout # Save a reference to the original standard output

with open('filename.txt', 'w') as f:
    sys.stdout = f # Change the standard output to the file we created.
    print(soup)
    sys.stdout = original_stdout # Reset the standard output to its original value


for productContainer in soup.findAll('li', class_='product-grid-product'):
  supplier = productContainer.find('a', class_='product-link').get(href)
  image = productContainer.find('img', class_='media-image').get('src')
  title = productContainer.find('img', class_='media-image').get('alt')
  #price = productContainer.find('span', class_='a8Pemb').text

  data.append({
    "Title": title,
    #"Price": price,
    "Supplier": supplier,
    "Image": image,
  })

print(json.dumps(data, indent = 2, ensure_ascii = False))
