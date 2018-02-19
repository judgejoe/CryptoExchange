from flask import Flask, render_template, Response, send_from_directory
import sqlalchemy as sa
from flask import json, request
from sqlalchemy.orm import sessionmaker
from objects import User, Transaction, Currency, Holding

sqlite_file = '../db/cryptoexchange.db'
engine = sa.create_engine('sqlite:///' + sqlite_file)
Session = sessionmaker(bind=engine)
session = Session()

our_user = session.query(User).filter_by(id=1).first()

trade = Transaction(transaction_type=0, user_id=2,currency_id=2,quantity=1)

session.add(trade)
our_trade = session.query(Transaction).first() 
session.commit()

app = Flask(__name__)
@app.route("/")
def main():
    return "Welcome!"

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/currencies/', methods=['GET'])
def currencies():
    rjson = []

    for row in session.query(Currency).all():
	rjson.append({'currency_id': row.id, 'code' : row.code})	

    js = json.dumps(rjson)

    resp = Response(js, status=200, mimetype='application/json')

    return resp

@app.route('/holdings/<int:user_id>', methods=['GET'])
def holdings(user_id):
    rjson = []

    for row in session.query(User).filter_by(id=user_id).one().holdings:
	rjson.append({'currency_id': row.currency.id, 'code' : row.currency.code, 'quantity' : row.quantity})	

    js = json.dumps(rjson)

    resp = Response(js, status=200, mimetype='application/json')

    return resp

@app.route('/trades', methods=['POST'])
def trade():
    rjson = {'quantity' : 0, 'currency_id' : -1, 'price' : -1, 'trade_currency' : -1}
    bitcoin_price = 120000
    print(request.method)
    if request.method == 'POST':
    	user_id = int(request.form['user_id'])
        currency_id = int(request.form['currency_id'])
	quantity = float(request.form['quantity'])
	trade_type = int(request.form['trade_type'])
	user = session.query(User).filter_by(id=user_id).first()

	if currency_id == 1:
	    trade_currency = 2
    	    asset_price = .001
	elif currency_id == 2:
	    trade_currency = 1
    	    asset_price = 12000
	elif currency_id == 3:
            trade_currency = 2
    	    asset_price = .2
	elif currency_id == 4:
	    trade_currency = 2
    	    asset_price = .5
 
    	trade_currency_holdings = session.query(Holding).filter_by(currency_id=trade_currency,user_id=user_id).first()
	if  asset_price * quantity <= trade_currency_holdings:
	    print('In trading block')
	    rjson['quantity'] = quantity
	    rjson['trade_type'] = trade_type
	    rjson['trade_currency'] = trade_currency
	    rjson['asset_price'] = asset_price
	    status = 200

    js = json.dumps(rjson)

    resp = Response(js, status=status, mimetype='application/json')

    return resp

@app.route('/trade')
def showHoldings():
    return render_template('trade.html')

if __name__ == "__main__":
    user = session.query(User).filter_by(id=2).first()
    print("User : " + str(user))
    app.run(host='0.0.0.0',port=8888)
