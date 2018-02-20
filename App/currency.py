import time
import requests
import json

# Globals == BAD. These aren't thread safe, and generally lead to bad code, but due to time constraints...
last_update_time = 0

prices = { }

def convert_currency(from_code, to_code, quantity):
    # Don't abuse the free API :)
    global last_update_time
    global prices
    now = time.time()
    if now - last_update_time > 60:
        resp = requests.request(
                method='GET',
                url='https://min-api.cryptocompare.com/data/pricemulti',
                params={'fsyms' : 'USD,BTC,LTC,DOGE,XMR', 'tsyms' : 'USD,BTC'},
                allow_redirects=False)
        last_update_time=now
        prices = json.loads(resp.content)
    return prices[from_code][to_code] * quantity

if __name__ == '__main__':
    print(convert_currency('BTC','USD', 1))
    print(convert_currency('LTC','BTC', 1))
