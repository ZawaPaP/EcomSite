from flask import Flask, render_template, request, redirect, url_for, session
import hashlib, os
import stripe
from user_db import add_data as user_add_data
from stripe_csv_to_db import get_data as products_get_data
from stripe_csv_to_db import get_item_by_productID as get_item_by_productID
from datetime import timedelta 
from os.path import join, dirname
from dotenv import load_dotenv

# This is your test secret API key.
load_dotenv('.env')
stripe.api_key = os.environ.get("Stripe_API_KEY")
YOUR_DOMAIN = 'http://localhost:4242'

app = Flask(__name__, 
            static_url_path='',
            static_folder='templates')

app.secret_key = os.environ.get("Flask_session.secret_key")
app.permanent_session_lifetime = timedelta(hours=3)

@app.route("/", methods = ['GET'])
def index():
    cart_items_number = 0
    if 'cart_items' in session:
        cart_items_number = len(session['cart_items'])
        
    
    products = products_get_data()
    for product in products:
        product["Amount"] = currency_formatter(product["Amount"], product["Currency"])
    return render_template('index.html', products=products, cart_items_number = cart_items_number)

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
    item = get_item_by_productID(product_id)
    session.permanent = True 
    session["id"] = product_id
    if 'cart_items' not in session:
        session['cart_items'] = []
    cart_list = session['cart_items']
    cart_list.append(item[0])
    session['cart_items'] = cart_list
    return redirect("/")

@app.route("/checkout", methods = ['GET', 'POST'])
def checkout():
    items = session['cart_items']
    for item in items:
        item["Amount"] = currency_formatter(item["Amount"], item["Currency"])
    return render_template('checkout.html', items = items)

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    if 'cart_items' not in session:
        redirect("/checkout")
    try:
        items = []
        cart_items = session['cart_items']
        for item in cart_items:
            items.append({'price': item["Price ID"], 'quantity': 1,})
        checkout_session = stripe.checkout.Session.create(
            line_items = items,
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