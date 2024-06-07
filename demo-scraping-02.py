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
  # print(link_elements)
  # check link href to avoid empty and external urls
  urls = []
  a_hrefs = []
  for link_element in link_elements:
    # if condition use to remove all a[href] empty
    if link_element.h2 and link_element.span and link_element.img:
      a_hrefs.append(link_element)
    
  # print(len(a_hrefs))
  # print(a_hrefs)
  for a_href in a_hrefs:
    product = {}
    product['url'] = a_href['href']
    product["name"] = a_href.h2.get_text()
    product['image'] = a_href.img['src']
    product['price'] = a_href.span.get_text()
    # append dict product to list products
    products.append(product)
  print(products)

# initialize the csv output file
with open('products.csv', 'w') as csv_file:
  writer = csv.writer(csv_file)

  # populating the CSV
  for product in products:
      writer.writerow(product.values())
      
# print(products)