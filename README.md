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

## Scope
Given the time constraints and limited speficifation I needed to aggressively minimize scope. Whenever a tradeoff needed to be made, I almost always favored getting core functionality working over anything else. Here are some of the assumptions that were made:
- There exists a market maker to facilitate trades. All trades will be made with the market maker at the current market price of the asset being traded. ONLY market orders are supported and the market maker will NEVER refuse a trade at market value. Traders will NOT trade directly with one another.
- The authoritative source for market prices for all cryptocurrencies will be the cryptocompare.com API.
- Currency prices are updated once an minute.
- There is no mimimum unit of currency. If a trader wants to buy .00000000000000000001 bitcoins, they can. The only limits are those imposed by the types in Javascript and Python. This is not how real-life trading generally works. Shares or units of currency must be purchased.
- Concurrency is not supported. Flask is run in single synchronous server on a single thread. Making the server thread safe would be a significant underatking
- Very small request loads are assumed. a few requests per second max.
- Security is not a requirement. PWs are stored in the clear. No SSL. No authentication. These would all be critically important requirements for a production, internet-scale web app but given time constraints it wasn't possible to implement proper security.

## Tech stack
## Server
Python/Flask was used as the application server give it's simplicity, ease of use, templating, quick setup time, and interoperability with DBs. Flask is also the web server in this setup. This would not be ideal in a real, internet-scale web app. For that you would want a web server in front of flask such as nginx or Apache. SQLAlchemy was used to access the database from within Flask. Several API endpoints were implement to implement retrieving balances, retrieving currency prices, converting between currencies, and making trades

## Database
SQLite was used as the Database System due to it's simplicity, ease of use, and quick setup time. SQLite would not scale to thousands of users, but a low QPS is assumed. SQLite is used in single-thread mode, and a single connection from the application server to the database is used.

## Front End
JQuery and Javacript approach used for client side scripting. There is no CSS. Functionality was prioritized over looks.


## Setup
The github repo contains a `setup` directory. In that directory is a setup script which handles installation of debian packages, pip packages, and database setup.  The following was run on an AWS t2.micro instance running the Ubuntu AMI (ami-66506c1c).
```ubuntu@ip-10-0-0-11:~/CryptoExchange$ cd setup/
ubuntu@ip-10-0-0-11:~/CryptoExchange/setup$ bash setup.sh 
Hit:1 http://us-east-1.ec2.archive.ubuntu.com/ubuntu xenial InRelease
Get:2 http://us-east-1.ec2.archive.ubuntu.com/ubuntu xenial-updates InRelease [102 kB]
Get:3 http://us-east-1.ec2.archive.ubuntu.com/ubuntu xenial-backports InRelease [102 kB]
Get:4 http://security.ubuntu.com/ubuntu xenial-security InRelease [102 kB] 
.
.
.
```

## Running the app
```ubuntu@ip-10-0-0-11:~/CryptoExchange/setup$ cd ../App/
ubuntu@ip-10-0-0-11:~/CryptoExchange/App$ python app.py 
* Running on http://0.0.0.0:8888/ (Press CTRL+C to quit)
```
Note that the server runs on port 8888.

## Using the app
There are 3 sections of the app:
- Holdings (/holdings) - This shows the users cryptocurrency holdings
- Currency Prices (/prices) - This shows the trading prices and conversion rates for tradeable currecies
- Trade (/trade) - This section allows the user to execute trades

Navigate to http://ec2-52-3-126-157.compute-1.amazonaws.com:8888/myholdings. You will be redirected to the login page.
There are 4 users: Jim, Bob, Lucy and Sally. Password is the same as the user name

![login](https://github.com/judgejoe/CryptoExchange/blob/dev/imgs/login.png)

Once you are logged in you will be redirected to the holdings page. On this page you will see all of the user's holdings, and their value in USD.

![holdings](https://github.com/judgejoe/CryptoExchange/blob/dev/imgs/holdings.png)

Say you want to check the prices of Bitcoin, or any other cryptocurrency.  Click on the "Currency Prices" link. That will bring you to a page which shows you all crypto curenncies supported in the platform and their price in USD and BTC.

![prices](https://github.com/judgejoe/CryptoExchange/blob/dev/imgs/currency_prices.png)

Now you decide you want to but some bitcoins. Go to Trade. Enter the amount you want to pay, select 'USD' from the drop down, then select the currency you want to receive. The amount you can buy of that currency will be auto populated based on the amount you entered.

![trade](https://github.com/judgejoe/CryptoExchange/blob/dev/imgs/TradeUSD_for_BTC.png)

Click Submit. You will be brought back to the holdings screen and your holdings will reflect your trade.

![Holdings_w_BTC](https://github.com/judgejoe/CryptoExchange/blob/dev/imgs/Holdings_w_BTC.png)

Go back to the Trades screen and attempt to trade $1000000 for bitcoin. You will get an error message.

![Insufficient Fund](https://github.com/judgejoe/CryptoExchange/blob/dev/imgs/insufficient_funds.png)

Now try and trade 1$ USD for Litecoins. You will receive an error again:

![Invalid Trade](https://github.com/judgejoe/CryptoExchange/blob/dev/imgs/invalid_trade.png)

## Testing
Test coverage is limited to a few unit tests (`tests/`) using Python's unittest module and several end-to-end tests exercising core functionality. With more time, unit testing coverage would be extended to cover all functions

## Future Enhancements
My app very much focuses on delivering core functionality at the expense of everything else. With more time, the following enhancements would be made:
- Scalability. Multithreading to support simultaneous user requests, making the code thread safe, putting nginx in front of the application server (i.e. to handle static file serving and other web server functions), using a more scalable database system
- Security. There is no security in his app. With more time I would use SSL, implement better password management, authenticate users making trades.
- Testing. Unit test coverage is pretty low as is. More unit tests would be needed to make this a reliable app
- Styling.
- Error handling. Error handling is good in some areas and not so good in others.  For example, if you try to trade with an invalid user id, you get an error message and a 4xx HTTP status.  If you omit a parameter from an api call to flask, you get a 405 Error with no indication of what went wrong.
- Revisit the 'holdings' calculation. To keep things as simple as possible and prevent potential out-of-sync errors, I chose NOT to store balances in the database. Instead when balances are computed, the entire transaction history is summed. This is ok for this app since the number of transactions is quite small. However this approach would be slow if the number of transactions becomes very large.
- Implement minimum currency unit & Floating point arithmetic. Bitcoin allows you to trade in units of .00000001 BTC. My app allows you to trade any fraction of a bitcoin that can be expressed as a floating point. I also used floats to keep things simple, but this introduces issues as many decimals cannot be represented as binary fractions and you end up with tiny amounts being added to your float values. A better approach would be to stay in the integer realm and trade in units of minimum currency units or to round floats. I just didn't get around to this.
