import time
import requests
import json

# Globals == BAD. These aren't thread safe, and generally lead to bad code, but due to time constraints...
last_update_time = 0
update_prices = True
prices = { }

def convert_currency_code(from_code, to_code, quantity):
    """
    convert a quantity of one crypto currency to another based on the current exchange rate

    :param from_code: the cryptocurrency code you are converting from
    :param to_code: the cryptocurrency code you are converting to
    :param quantity: the amount of the "from" currency you wish to convery
    :returns: the quantity of "to" currency that "from" currency is worth based on current exchange rates
    """
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
    """
    Helper function that returns whether two cryptocurrencies are allowed to be traded on the platform

    :param from_code: the cryptocurrency code you are converting from
    :param to_code: the cryptocurrency code you are converting to
    :returns: True if the currencies are allowed to be traded, false otherwise.
    """
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
