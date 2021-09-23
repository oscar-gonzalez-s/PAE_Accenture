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
  'https://www.google.com/search?q=camiseta+blanca+flores&tbm=shop',
  headers=headers).text

soup = BeautifulSoup(response, 'lxml')


data = []

original_stdout = sys.stdout # Save a reference to the original standard output

with open('filename.txt', 'w') as f:
    sys.stdout = f # Change the standard output to the file we created.
    print(soup)
    sys.stdout = original_stdout # Reset the standard output to its original value


for productContainer in soup.findAll('div', class_='sh-pr__product-results-grid'):
  title = productContainer.find('h4', class_='Xjkr3b').text
  #price = productContainer.find('span', class_='a8Pemb').text
  supplier = productContainer.find('a', class_='xCpuod').get(href)
  #image = productContainer.find('div', class_='Ar0c1c').find('img')

  data.append({
    "Title": title,
    #"Price": price,
    "Supplier": supplier,
  })

print(json.dumps(data, indent = 2, ensure_ascii = False))
