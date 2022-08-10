import requests
from bs4 import BeautifulSoup
import math
import pandas as pd

# User-Agent got by typing "my user agent" at Google
headers = {'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

city = 'dublin-city'

def get_number_of_pages(city, headers):
    r = requests.get(f'https://www.daft.ie/property-for-sale/{city}?pageSize=20', headers)
    html = BeautifulSoup(r.content, 'html.parser')
    number_of_houses = int(html.find('h1').text.split()[0].replace(',', ''))  
    pagination = math.ceil(number_of_houses/20)
    return number_of_houses, pagination

def get_houses(city, headers):

    number_of_houses, pagination = get_number_of_pages(city, headers)

    price_list = []
    address_list = []
    beds_list = []
    baths_list = []
    floor_area_list = []
    property_type_list = []

    print(f'Scrapping Pages...')

    for i in range(pagination):
        print(i+1)
        
        r = requests.get(f'https://www.daft.ie/property-for-sale/{city}?pageSize=20&from={i * 20}', headers)
        html = BeautifulSoup(r.content, 'html.parser')

        card_bodies = html.find_all(attrs={"data-testid": "card-body"})

        for card in card_bodies:
            try:
                price_list.append(card.find(attrs={"data-testid": "price"}).text[1:])
            except:
                price_list.append('')
            try:
                address_list.append(card.find(attrs={"data-testid": "address"}).text)
            except:
                address_list.append('')
            try:
                beds_list.append(card.find(attrs={"data-testid": "beds"}).text)
            except:
                beds_list.append('')
            try:
                baths_list.append(card.find(attrs={"data-testid": "baths"}).text)
            except:
                baths_list.append('')
            try:
                floor_area_list.append(card.find(attrs={"data-testid": "floor-area"}).text.replace('m²', ''))
            except:
                floor_area_list.append('')
            try:
                property_type_list.append(card.find(attrs={"data-testid": "property-type"}).text)
            except:
                property_type_list.append('')

    df = pd.DataFrame({  
        'address' : address_list,
        'beds' : beds_list,
        'baths' : baths_list,
        'floor_area' : floor_area_list,
        'property_type' : property_type_list,
        'price' : price_list,
    })

    df.to_csv(f'model/{number_of_houses}_{city}_houses_df.csv', index=False)

    return df

if __name__ == '__main__':  
    df = get_houses(city, headers)



