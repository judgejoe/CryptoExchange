from flask import Flask, render_template, Response, send_from_directory
import sqlalchemy as sa
from flask import json, request
from sqlalchemy.orm import sessionmaker
from objects import User, Transaction, Currency, Holding

sqlite_file = '../db/cryptoexchange.db'
engine = sa.create_engine('sqlite:///' + sqlite_file)
Session = sessionmaker(bind=engine)
session = Session()

prices = {
	"BTC"  : {"USD" : 10557.2},
	"LTC"  : {"BTC":0.02056,"USD":217.29},
	"DOGE" : {"BTC":6.1e-7,"USD":0.006542},
	"XMR"  : {"BTC":0.02863,"USD":303.03},
	"USD"  : {"BTC":0.0000947,"USD" : 1}
	}

app = Flask(__name__)

@app.before_request
def before_request():
    #update all crypto prices
    pass

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

    user = session.query(User).filter_by(id=user_id).scalar()
    if user == None:
        js = json.dumps(rjson)
        return Response(json.dumps({'error':'no user with id ' + str(user_id)}), status=400, mimetype='application/json')
    
    holdings = user.holdings
    if len(holdings) == 0:
        js = json.dumps(rjson)
        return Response('', status=204, mimetype='application/json')

    for row in holdings:
        value = prices[row.currency.code]["USD"] * row.quantity
        rjson.append({'currency_id': row.currency.id, 'code' : row.currency.code, 'quantity' : row.quantity, 'value': value})	

    resp = Response(json.dumps(rjson), status=200, mimetype='application/json')

    return resp

@app.route('/trades', methods=['POST'])
def trade():

    rjson = {'quantity' : 0, 'my_currency_id' : -1, 'trade_currency_id' : -1}

    user_id = 2 #int(request.form['user_id'])
    my_currency_id = int(request.form['my_currency_id'])
    trade_currency_id = int(request.form['trade_currency_id'])
    quantity = float(request.form['quantity'])
    user = session.query(User).filter_by(id=user_id).first()
    my_currency_code = session.query(Currency).filter_by(id=my_currency_id).first().code
    trade_currency_code = session.query(Currency).filter_by(id=trade_currency_id).first().code 

    if trade_currency_code == 'BTC':
        if my_currency_code != 'USD':
            return Response(json.dumps({'error' : 'Cannot trade ' + str(my_currency_code) + ' for ' + str(trade_currency_code)}), status=403, mimetype='application/json')
    if trade_currency_code == 'USD' or trade_currency_code == 'LTC' or trade_currency_code == 'DOGE' or trade_currency_code == 'XMR':
        if my_currency_code != 'BTC':
            return Response(json.dumps({'error' : 'Cannot trade ' + str(my_currency_code) + ' for ' + str(trade_currency_code)}), status=403, mimetype='application/json')

    my_currency_holdings = session.query(Holding).filter_by(currency_id=my_currency_id,user_id=user_id).first().quantity
    if  prices[trade_currency_code][my_currency_code] * quantity <= my_currency_holdings:
        rjson['my_currency_holdings'] = my_currency_holdings
        rjson['quantity'] = quantity
        rjson['trade_currency_id'] = trade_currency_id
        rjson['my_currency_id'] = my_currency_id
        rjson['price'] = prices[trade_currency_code][my_currency_code] * quantity
        return Response(json.dumps(rjson), status=200 , mimetype='application/json')
    else:
        return Response(json.dumps({'error' : 'Insufficient funds'}), status=403, mimetype='application/json')


@app.route('/holdings')
def showHoldings():
    return render_template('holdings.html')

@app.route('/trade')
def showTrade():
    return render_template('trade.html')

if __name__ == "__main__":
    user = session.query(User).filter_by(id=2).first()
    app.run(host='0.0.0.0',port=8888)
