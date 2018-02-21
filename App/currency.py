import time
import requests
import json

# Globals == BAD. These aren't thread safe, and generally lead to bad code, but due to time constraints...
last_update_time = 0
update_prices = True
prices = { }

def convert_currency_code(from_code, to_code, quantity):
    global last_update_time
    global prices

    # Don't abuse the free API :)
    now = time.time()
    if now - last_update_time > 60 and update_prices:
        resp = requests.request(
                method='GET',
                url='https://min-api.cryptocompare.com/data/pricemulti',
                params={'fsyms' : 'USD,BTC,LTC,DOGE,XMR', 'tsyms' : 'USD,BTC,LTC,DOGE,XMR'},
                allow_redirects=False)
        last_update_time=now
        prices = json.loads(resp.content)
    return float(prices[from_code][to_code]) * float(quantity)

def tradeable_currency_codes(from_code, to_code):
    if to_code == 'BTC':
        if from_code != 'USD' and \
           from_code != 'LTC' and \
           from_code != 'DOGE' and \
           from_code != 'XMR':
            return False
    if to_code == 'USD'  or \
       to_code == 'LTC'  or \
       to_code == 'DOGE' or \
       to_code == 'XMR':
        if from_code != 'BTC':
            return False
    return True

if __name__ == '__main__':
    print(convert_currency('BTC','USD', 1))
    print(convert_currency('LTC','BTC', 1))
