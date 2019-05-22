import os
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs


def get_products(dir_name, amount=np.inf):
    '''return list of filenames with product pages'''
    products = []
    path_upper = dir_name + '/categories/'
    categories = os.listdir(path_upper)
    for cat in categories:
        path_lower = path_upper + cat
        path_list = [path_lower + '/' + i for i in os.listdir(path_lower)]
        products.extend(path_list)
    if amount==np.inf:
        return products
    else:
        return products[:amount]


def product_to_soup(product):
    '''open product file, create beautifulsoup'''
    p = open(product, 'rb').read()
    s = bs(p, 'lxml')
    return s
    

for dir_name in [i for i in os.listdir() if i.startswith('201')]:
    products = get_products(dir_name)
    
    # Create empty dataframe
    df = pd.DataFrame()
    
    # Loop through products in directory
    for product in products:
        soup = product_to_soup(product)

        for i in [vendor.text for vendor in soup.select('div.vendor')]:
            if i.find('sold by \n') != 1:
                #DO SOMETHING TO REPLACE I WITH -
        
        try:
            titles = [i.text for i in soup.select('div.item_title')]
            prices = [i.text for i in soup.select('div.price')]
            shipping = [i.text.strip().split('\n') for i in soup.select('div.shipping')]
            ships_from = [i[0].strip().split()[2] for i in shipping]
            ships_to = [i[1].strip().split()[2] for i in shipping]
            rating_count = [i.text[1:-1] for i in soup.select('div.rating_count')]
            member_name = [i.text for i in soup.select('div.vendor a')]
            member_rating = [i.text for i in soup.select('span.vendor_rating')]
            
            # not all html follow same structure
            if not member_rating:
                titles = [i.text for i in soup.select('div.item_title')]
                prices = [i.text for i in soup.select('div.price_big')]
                item_details = [i.text.strip().split('\n') for i in soup.select('div.item_details')]
                member_name = [i[0][8:] for i in item_details]
                ships_from = [i[1].strip()[12:] for i in item_details]
                ships_to = [i[2].strip()[10:] for i in item_details]
                rating_count = ['nan' for i in titles] #not existing in this data
                member_rating = ['nan' for i in titles] #not existing in this data
        except IndexError:
            pass
        
        _df = pd.DataFrame({
            'product':titles,
            'prices':prices,
            'ships_from':ships_from,
            'ships_to':ships_to,
            'rating_count':rating_count,
            'member_name':member_name,
            'member_rating':member_rating
            })
    
        df = df.append(_df)
    
    df.reset_index(inplace=True, drop=True)
