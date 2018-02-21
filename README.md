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
* There exists a market maker to facilitate trades. All trades will be made with the market maker at the current market price of the asset being traded. ONLY market orders are supported and the market maker will NEVER refuse a trade at market value. Traders will NOT trade directly with one another.
* The authoritative source for market prices for all cryptocurrencies will be the cryptocompare.com API.
* Currency prices are updated once an minute.
* There is no mimimum unit of currency. If a trader wants to buy .00000000000000000001 bitcoins, they can. The only limits are those imposed by the types in Javascript and Python. This is not how real-life trading generally works. Shares or units of currency must be purchased.
* Concurrency is not supported. Flask is run in single synchronous server on a single thread. Making the server thread safe would be a significant underatking
* Very small request loads are assumed. a few requests per second max.
* Security is not a requirement. PWs are stored in the clear. No SSL. No authentication. These would all be critically important requirements for a production, internet-scale web app but given time constraints it wasn't possible to implement proper security.

## Tech stack
## Server
Python/Flask was used as the application server give it's simplicity, ease of use, templating, quick setup time, and interoperability with DBs. Flask is also the web server in this setup. This would not be ideal in a real, internet-scale web app. For that you would want a web server in front of flask such as nginx or Apache. SQLAlchemy was used to access the database from within Flask.

## Database
SQLite was used as the Database System due to it's simplicity, ease of use, and quick setup time. SQLite would not scale to thousands of users, but a low QPS is assumed. SQLite is used in single-thread mode, and a single connection from the application server to the database is used.

## Front End
JQuery and Javacript approach used for client side scripting. There is no CSS. Functionality was prioritized over looks.

## Setup
The github repo contains a `setup` directory. In that directory is a setup script which handles installation of debian packages, pip packages, and database setup.  The following was run on an AWS t2.micro instance running the Ubuntu AMI (ami-66506c1c).
`$ cd setup
$ bash setup

## Running the app
cd ../App
$ python app.py

Note that the server runs on port 8888.

## Using the app
There are 3 sections of the app:
- Holdings (/holdings) - This shows the users cryptocurrency holdings
- Currency Prices (/prices) - This shows the trading prices and conversion rates for tradeable currecies
- Trade (/trade) - This section allows the user to execute trades

Navigate to http://ec2-52-3-126-157.compute-1.amazonaws.com:8888/myholdings. You will be redirected to the login page.
There are 4 users: Jim, Bob, Lucy and Sally. Password is the same as the user name

<photo of login here>

Once you are logged in you will be redirected to the holdings page. On this page you will see all of the user's holdings, and their value in USD.

<photo of holdings here>

Say you want to check the prices of Bitcoin, or any other cryptocurrency.  Click on the "Currency Prices" link. That will bring you to a page which shows you all crypto curenncies supported in the platform and their price in USD and BTC.

<photo of currency prices here>

Now you decide you want to but some bitcoins. Go to Trade

<photo of trading screen here>

Enter the amount you want to pay, select 'USD' from the drop down, then select the currency you want to receive. The amount you can buy of that currency will be auto populated based on the amount you entered.

<photo of autopopulation>

Click Submit. You will be brought back to the holdings screen and your holdings will reflect your trade.

<photo of holdings>

Go back to the Trades screen and attempt to trade $1000000 for bitcoin. You will get an error message.

<photo of insufficient funds error>

Now try and trade 1$ USD for Litecoins. You will receive an error again:

<photo Invalid trade error>

