from flask import Flask, render_template, request, redirect, url_for
import hashlib
import json
import stripe
from user_db import add_data as user_add_data
from stripe_csv_to_db import get_data as products_get_data

# This is your test secret API key.
stripe.api_key = 'sk_test_51MZbIFA9Qashsbv2iR7UnyIYHgP78XhB1gZRqZQ8mozqCCGabK47D3MnIyEzhUiABXvX73CZ2nJZRMbJwgqBYJGE00Cgi5aOoP'
YOUR_DOMAIN = 'http://localhost:4242'


app = Flask(__name__, 
            static_url_path='',
            static_folder='templates')

@app.route("/", methods = ['GET'])
def index():
    products = products_get_data()
    for product in products:
        product["Amount"] = currency_formatter(product["Amount"], product["Currency"])
    return render_template('index.html', products=products)

@app.route("/registration", methods = ['GET', 'POST'])
def registration():
    return render_template('registration.html')


@app.route("/complete-registration", methods = ['POST'])
def complete_registration():
    fn = request.form.get('firstName')
    ln = request.form.get('lastName')
    em = request.form.get('email')
    ph = request.form.get('phone')
    address = request.form.get('address')
    address2 = request.form.get('address2')
    
    user = {
        'fn': fn, 
        'ln': ln,
        'em': em, 
        'ph': ph, 
        'address': hash(address),
        'address2': hash(address2)  
    }
    # create new user data 
    user_add_data(user)
    return render_template('checkout.html')

@app.route("/cart/<product_id>", methods=['POST'])
def add_to_cart(product_id):
    print(product_id)
    return render_template('registration.html')

@app.route("/checkout", methods = ['GET', 'POST'])
def checkout():
    #item = json.loads(request.form.get('select_item'))
    return render_template('checkout.html')

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1MZvCsA9Qashsbv2nKMBjfu7',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success.html',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
            automatic_tax={'enabled': False},
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)


@app.route("/success")
def success():
    return render_template('success.html')

@app.route("/cancel")
def cancel():
    return render_template('cancel.html')

def hash(string):
    return hashlib.sha256(string.encode('utf-8')).hexdigest()

def currency_formatter(value, curr):
    curr = curr.upper()
    price = "{}  {:,.2f}".format(curr,value)
    return price

if __name__ == '__main__':
    app.run(port=4242)