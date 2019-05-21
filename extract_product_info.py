import os
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs


def get_products(dir_name, amount=np.inf):
    '''return list of filenames with product pages'''
    path = dir_name + '/market'
    files = os.listdir(path)
    products = [path + '/' + i for i in files if i.startswith('viewProduct')]
    if amount==np.inf:
        return products
    else:
        return products[:amount]


def product_to_soup(product):
    '''open product file, create beautifulsoup'''
    p = open(product, 'rb').read()
    s = bs(p, 'lxml')
    return s
    

dir_name = input('type the name of the directory here: ')
products = get_products(dir_name)

# Create empty lists for gathering info
product_index = []
product_title = []
member_name = []
successful_transactions = []
seller_status = []
extended_info = []

# Loop through products in directory
for i, product in enumerate(products):
    soup = product_to_soup(product)
    
    product_index.append(i)
    product_title.append(soup.select('div.title')[0].string)
    member_name.append(soup.select('div.tabularDetails a')[0].text.strip())
    successful_transactions.append(soup.select('div.tabularDetails a')[1].text.strip())
    seller_status.append(soup.find('span', {'class':'sellerStatus'})['title'])
    extended_info.append(soup.select('#offerDescription')[0].text.strip())


# Bundle data in dataframe
df = pd.DataFrame({'product':product_title,
    'seller': member_name,
    'successful_transactions':successful_transactions,
    'seller_status':seller_status,
    'info':extended_info})
