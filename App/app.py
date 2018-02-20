from flask import Flask, render_template, Response, send_from_directory,redirect, url_for, make_response
import sqlalchemy as sa
from flask import json, request
from sqlalchemy.orm import sessionmaker
from objects import User, Transaction, Currency, Holding
from currency import convert_currency_code, tradeable_currency_codes
from sqlalchemy.sql import functions as func
import requests

sqlite_file = '../db/cryptoexchange.db'
engine = sa.create_engine('sqlite:///' + sqlite_file)
Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)


@app.before_request
def before_request():
    if 'login_user_id' not in request.cookies.keys() and request.endpoint != 'login':
        return redirect(url_for('login'))

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        user = session.query(User).filter_by(name=username).filter_by(password=password).scalar()
        if user is None:
            response = make_response(json.dumps({error:'Invalid username or password'}))
            response.status_code=403
            response.mime_type='application/json'
            return response
        else:
            response = make_response(redirect(url_for('showHoldings')))
            response.set_cookie('login_user_id',str(user.id),max_age=86400)
            return response

@app.route('/currencies/', methods=['GET'])
def currencies():
    rjson = []

    for row in session.query(Currency).all():
        rjson.append({'id': row.id, 'code' : row.code, 'value_usd' : convert_currency_code(row.code, 'USD', 1), 'value_btc': convert_currency_code(row.code, 'BTC', 1)})	

    js = json.dumps(rjson)

    resp = Response(js, status=200, mimetype='application/json')

    return resp

def get_currency_balance(user_id, currency_code): 
    transactions = session.query(Transaction, func.sum(Transaction.amount).label('balance')).filter_by(user_id = user_id).join(Currency).filter_by(code = currency_code).group_by(Transaction.currency_id).one()
    if len(transactions) == 0:
        return []
    return transactions

def get_balances(user_id): 
    transactions = session.query(Transaction, func.sum(Transaction.amount).label('balance')).filter_by(user_id = user_id).join(Currency).group_by(Transaction.currency_id).all()
    if len(transactions) == 0:
        return []
    return transactions

@app.route('/holdings/', methods=['GET'])
def holdings():
    rjson = []

    user_id = request.cookies['login_user_id']
    user = session.query(User).filter_by(id=user_id).scalar()
    if user == None:
        js = json.dumps(rjson)
        return Response(json.dumps({'error':'no user with id ' + str(user_id)}), status=400, mimetype='application/json')
    
    balances = get_balances(user_id)
    for row in balances:
        print(row)
        rjson.append({'currency_id' : row.Transaction.currency.id, 'currency_code' : row.Transaction.currency.code, 'quantity' : row.balance, 'value': convert_currency_code(row.Transaction.currency.code, 'USD', row.balance)})	
    
    resp = Response(json.dumps(rjson), status=200, mimetype='application/json')

    return resp


@app.route('/trades/', methods=['POST'])
def trade():

    rjson = {'quantity' : 0, 'from_currency_id' : -1, 'to_currency_id' : -1}

    user_id             = request.cookies['login_user_id']
    from_currency_id    = int(request.form['from_currency_id'])
    to_currency_id      = int(request.form['to_currency_id'])
    from_quantity       = float(request.form['from_quantity'])
    user                = session.query(User).filter_by(id=user_id).first()
    from_currency_code  = session.query(Currency).filter_by(id=from_currency_id).first().code
    to_currency_code    = session.query(Currency).filter_by(id=to_currency_id).first().code 
    transaction_type_id = 3 

    # Check that these currencies are tradeable. Users are allowed to trade USD <-> BTC and BTC <-> (LTC|DOGE|XMR)
    if not tradeable_currency_codes(from_currency_code,to_currency_code):
        return Response(json.dumps({'error' : 'Cannot trade ' + str(from_currency_code) + ' for ' + str(to_currency_code)}), 
                        status=403, 
                        mimetype='application/json')


    balance = get_currency_balance(user_id, from_currency_code)
    if from_quantity <= balance.balance:
        to_quantity = convert_currency_code(from_currency_code, to_currency_code, from_quantity)
        rjson['to_currency_id']     = to_currency_id
        rjson['from_currency_id']   = from_currency_id
        new_debit                   = Transaction(transaction_type_id = 3,
                                                  user_id             = user_id, 
                                                  currency_id         = from_currency_id, 
                                                  amount              = -1 * from_quantity)
        new_credit                  = Transaction(transaction_type_id = 3,
                                                  user_id             = user_id, 
                                                  currency_id         = to_currency_id, 
                                                  amount              = to_quantity)
        session.add(new_debit)
        session.add(new_credit)

        session.commit()
        return Response(json.dumps(rjson), status=200 , mimetype='application/json')
    else:
        return Response(json.dumps({'error' : 'Insufficient funds'}), status=403, mimetype='application/json')


@app.route('/prices')
def showPrices():
    return render_template('currencies.html')

@app.route('/myholdings')
def showHoldings():
    return render_template('holdings.html')

@app.route('/trade')
def showTrade():
    return render_template('trade.html')
 
@app.route('/convert_currency/', methods=['POST'])
def convertCurrency():
    from_currency_id = request.form['from_currency_id']
    to_currency_id   = request.form['to_currency_id']
    quantity         = request.form['from_quantity']

    from_currency_code = str(session.query(Currency).filter_by(id=from_currency_id).one().code)
    to_currency_code = str(session.query(Currency).filter_by(id=to_currency_id).one().code)
    conversion = convert_currency_code(from_currency_code, to_currency_code, quantity)

    return Response(json.dumps({'from_currency_id' : from_currency_id, 'to_currency_id' : to_currency_id, 'quantity_from' : quantity, 'quantity_to' : conversion} ), status=200 , mimetype='application/json')


@app.route('/data/pricemulti', methods=['GET'])
def _proxy(*args, **kwargs):
    resp = requests.request(
            method=request.method,
            url=request.url.replace('http://','https://')
                           .replace(request.headers['Host'], 'min-api.cryptocompare.com'),
            headers={key: value for (key, value) in request.headers if key != 'Host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False)

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
            if name.lower() not in excluded_headers]

    response = Response(resp.content, resp.status_code, headers)
    return response


if __name__ == "__main__":
    user = session.query(User).filter_by(id=2).first()
    app.run(host='0.0.0.0',port=8888)
