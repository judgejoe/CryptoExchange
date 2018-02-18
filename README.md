# CryptoExchange
CryptoExchange for Salt coding challenge

## User Stories
### Trade USD for Bitcoin
As a cryptocurrency trader, I want to trade my US Dollars for Bitcoin assets of equivalent value so that I can own Bitcoins as an asset and use them in future trades.
### Trade Bitcoin for an alternative currency
As a cryptocurrency trader, I want to trade my Bitcoins for Litecoins, Dogecoins, and Monero of equivalent value so that I can own those currencies as an asset and use them in future trades.
### Trade alternative currency for Bitcoins
As a cryptocurrency trader, I want to trade my Litecoins, Dogecoins, and Monero for Bitcoins of equivalent value so that I can own Bitcoins as an asset and use them in future trades.
### View cryptocurrency prices
As a cryptocurrency trader, I want to see the current price of Bitcoins (in USD), and Litecoins, Dogecoins, and Monero (in Bitcoins) so that I can make trading decisions
### View portfolio
As a crypto currency trader, I want to see my current Bitcoin, Litecoin, Dogecoin, and Monero holdings and their values in USD/Bitcoins so that I can make trading decisions.

## Constraints
To limit scope, I will assume the following constraints:
* There exists a market maker to facilitate trades. All trades will be made with the market maker at the current market price of the asset being traded. ONLY market orders are supported and the market maker will NEVER refuse a trade at market value. Traders will NOT trade directly with one another.
* The authoritative source for market prices for all cryptocurrencies will be the cryptocompare.com API.
* Currency prices are updated once an hour.
* Traders must have sufficient holdings to settle any trade they execute. There will be no automatic trading of crypto assets to cover trades. If a user wishes to buy $1000 of Bitcoin, they must have $1000 USD in their account. If a user wishes to buy 10 BTC of Litecoin, they must have 10 BTC in their account.
* No trading fees.
* Things like user management are omitted
## Tech stack


