import requests
import json
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import csv

# initializa the data structure to store the scrapped data
products = []

#  initialize the list of discoverd urls
urls_craw = ['https://www.scrapingcourse.com/ecommerce/']

# util all pages have been visited
while len(urls_craw) != 0:
  
  # get page to visit from the list
  current_url = urls_craw.pop()
  # print(current_url)
  response = requests.get(current_url)
  test_soup = BeautifulSoup(response.content, "html.parser")
  # print(soup)
  link_elements = test_soup.select("a[href]")
  print(link_elements)
  # check link href to avoid empty and external urls
  urls = []
  a_hrefs = []
  for link_element in link_elements:
    product = {}
    # if condition use to remove all a[href] empty
    if link_element.h2 and link_element.span and link_element.img:
      product['url'] = link_element['href']
      product["name"] = link_element.h2.get_text()
      product['image'] = link_element.img['src']
      product['price'] = link_element.span.get_text()
      # append dict product to list products
      products.append(product)

# initialize the csv output file
with open('products.csv', 'w') as csv_file:
  writer = csv.writer(csv_file)

  # populating the CSV
  for product in products:
      writer.writerow(product.values())
      
# print(products)