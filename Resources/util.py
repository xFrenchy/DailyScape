import requests
import os

from requests.api import request
from datetime import date, datetime

from Resources.Items import Item_Dict

api_url = "https://services.runescape.com/m=itemdb_rs/api/catalogue/"
G_RUNE_CATEGORY = 32    # category 32 is 'Runes, Spells and Teleports' for API request

def price_to_int(price):
    """Converts a string representation of a price into an integer
    For example, 15.3k will convert to 15_300 and 15m 15_000_000
    and returns the integer value"""
    multiplier = 1
    if 'k' in price:
        multiplier = 1_000
    elif 'm' in price:
        multiplier = 1_000_000
    # Nothing to split if there is no letter multiplier
    if multiplier != 1:
        return int(float(price[:-1]) * multiplier)
    else:
        return int(price.replace(',', ''))

def price_to_str(price):
    """Converts the int representation of a price into a string.
    For example, 15_300 will be 15.3k and 15_000_000 will be 15m
    and returns the string"""
    if price < 1000:
        return str(price) + "gp"
    else:
        million = int(price/1_000_000)
        price = price % 1_000_000
        thousand = int(price/1_000)
        price = price % 1_000
        # price is now the remainder under 1_000

        # https://stackoverflow.com/questions/8500374/python-statement-of-short-if-else
        return (str(million) + "." + str(thousand) + "m", str(thousand) + "." + str(price) + "k") [million == 0]

def retrieve_item(name, category):
    #TODO it's adding duplicates, this check must be checking an object instead of value, fix it
    if name not in Item_Dict.keys():
        # add this item in our dictionary
        item = search_item(name, category)
        add_item(name, item)
        return item 

    else:
        # two scenario here, key exists and is up to date, key exists and is old
        item = Item_Dict[name]
        if(item['date'] == date.isoformat(datetime.utcnow().date())):
            # woo we don't do an API call
            return item
        else:
            # damn still have to do an API call
            item = search_item(name, category)
            add_item(name, item)
            return item
            
def search_item(name, category):
    found = False
    page = 0

    while found != True:
        #TODO: error proof response from timeouts and other things that would make my code oopsie woopsie
        response = requests.get(api_url + "items.json?category=" + str(category) + "&alpha=" + name[0].lower() + "&page=" + str(page))
        
        if len(response.json()['items']) == 0:
            # items are empty, we have exhausted the list
            raise NameError(name + " not found")
        else:
            # Search result for given item
            for item in response.json()['items']:
                if item['name'] == name:
                    return item
        page += 1

def add_item(name, item):
    lines = []
    item['date'] = str_today = date.isoformat(datetime.utcnow().date())
    with open("Resources/Items.py", "r", encoding = "utf-8") as f:
        lines = f.readlines()
        lines = lines[:-1]  # remove last line since we're appending to the dictionary
    with open("Resources/Items.py", "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line)
        f.write("\'" + name + "\': " + str(item) + ",\n")
        f.write("}")
        f.close()

