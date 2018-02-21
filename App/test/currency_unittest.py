import unittest
import sys
sys.path.append("../")
from currency import tradeable_currency_codes

class TestTradeable(unittest.TestCase):
 
    def setUp(self):
        pass
    def test_USD_to_BTC(self):
        self.assertTrue(tradeable_currency_codes('USD','BTC'))
 
    def test_BTC_to_USD(self):
        self.assertTrue(tradeable_currency_codes('BTC','USD'))
 
    def test_BTC_to_LTC(self):
        self.assertTrue(tradeable_currency_codes('BTC','LTC'))
 
    def test_BTC_to_DOGE(self):
        self.assertTrue(tradeable_currency_codes('BTC','DOGE'))
 
    def test_BTC_to_XMR(self):
        self.assertTrue(tradeable_currency_codes('BTC','XMR'))
 
    def test_LTC_to_BTC(self):
        self.assertTrue(tradeable_currency_codes('LTC','BTC'))
 
    def test_DOGE_TO_BTC(self):
        self.assertTrue(tradeable_currency_codes('DOGE','BTC'))
 
    def test_XMR_TO_BTC(self):
        self.assertTrue(tradeable_currency_codes('XMR','BTC'))
 
    def test_USD_to_DOGE(self):
        self.assertFalse(tradeable_currency_codes('USD','DOGE'))
 
    def test_USD_to_XMR(self):
        self.assertFalse(tradeable_currency_codes('USD','XMR'))
 
    def test_USD_to_LTC(self):
        self.assertFalse(tradeable_currency_codes('USD','LTC'))
 
if __name__ == '__main__':
    unittest.main()
