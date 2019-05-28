import os
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs
import traceback


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


# Create iterator (i) to check the amount of iterations completed
i = 0

# Create empty dataframe for the data in all directories
df_full = pd.DataFrame()

# Loop over all subdirectories in directory
for dir_name in [i for i in os.listdir() if i.startswith('201')]:
    # Get list of filenames of products in subdirectory
    products = get_products(dir_name)
    
    # Create empty dataframe for the data in this directory
    df_dir = pd.DataFrame()
    
    # Loop through products in directory
    for product in products:
        p = open(product, 'r').read()

        # If there are any unknown seller names, replace empty value with '-'
        if p.find('sold by \n') != -1:
            p = p.replace('sold by \n', 'sold by <a href="unknown">-</a> \n')

        # Make soup with BeautifulSoup
        soup = bs(p, 'lxml')

        
        # find relevant information in html text
        try:
            titles = [i.text for i in soup.select('div.item_title')]
            prices = [i.text for i in soup.select('div.price')]
            shipping = [i.text.strip().split('\n') for i in soup.select('div.shipping')]
            ships_from = [i[0].split(':')[1] for i in shipping]
            ships_to = [i[1].split(':')[1].strip() for i in shipping]
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
        
        try:
            # Put data in dataframe
            _df = pd.DataFrame({
                'product':titles,
                'prices':prices,
                'ships_from':ships_from,
                'ships_to':ships_to,
                'rating_count':rating_count,
                'member_name':member_name,
                'member_rating':member_rating
                })
        except ValueError:
            # Print error when missing data results in size differences of arrays
            print('ValueError in: ' + product + '\n' + traceback.format_exc())
            continue
    
        # Append dataframe to dataframe containing all data of the subdirectory
        df_dir = df_dir.append(_df)
    
    # Append dataframe with subdirectory data to dataframe with all data in directory
    df_full = df_full.append(df_dir)
    df_full.reset_index(inplace=True, drop=True)

    i = i+1
    print('directory processed: ' + str(i) + '/' + str(len(os.listdir())) )


# Optionally save to csv file
save_to_csv = input('save output to csv? [y/n]: ')
if save_to_csv == 'y':
    df_full.to_csv('silkroad2_allproducts.csv')
else:
    print('Script completed, output not saved')
