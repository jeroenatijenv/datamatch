import os
import pandas as pd
from bs4 import BeautifulSoup as bs


# Define functions
def get_products(dir_name):
    '''return list of filenames with product pages'''
    products = [dir_name + '/' + i for i in os.listdir(dir_name) if 'item' in i]
    return products


# Run script
## Get list of product filenames
products = get_products('2014-02-14')
## Create empty dataframe for storing all data
df_full = pd.DataFrame()
for product in products:
    ## open the file
    html = open(product, 'r').read()

    ## Create soup with BeautifulSoup
    soup = bs(html, 'lxml')

    ## Select data from soup
    categorie = soup.select('ul.breadcrumb span')[1].text
    product = soup.select('ul.breadcrumb span')[2].text
    published = soup.select_one('em.publish').text.split(': ')[1]
    description = soup.select_one('#description').text.strip()
    try:
        ships_from = soup.select_one('#item_location').text.split(': ')[1]
    except IndexError:
        ships_from = 'unknown'
    member_name = soup.select_one('p.name a').text
    member_rating = soup.select('p.name b')[1].text
    amount_of_reviews = soup.select('p.name b')[2].text
    price_usd = soup.select('#sidebar b')[0].text
    price_btc = soup.select('#sidebar b')[1].text
    
    ## Combine data in dataframe
    _df = pd.DataFrame({
        'product':[product],
        'prices_usd':[price_usd],
        'prices_btc':[price_btc],
        'ships_from':[ships_from],
        'rating_count':[amount_of_reviews],
        'member_name':[member_name],
        'member_rating':[member_rating],
        'categorie':[categorie],
        'date_published':[published],
        'description':[description]
        })
    
    ## Combine dataframe with full dataframe
    df_full = df_full.append(_df)
