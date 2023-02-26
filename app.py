from flask import Flask, render_template,redirect, session
import hashlib
import os
import stripe
from stripe_csv_to_db import get_data as products_get_data
from stripe_csv_to_db import get_item_by_productID as get_item_by_productID
from datetime import timedelta
#from dotenv import load_dotenv

#load_dotenv('.env')
stripe.api_key = os.getenv('Stripe_API_KEY')
print("stripe.api_key: " + stripe.api_key)
YOUR_DOMAIN = 'https://ec-vuqv.onrender.com'

app = Flask(__name__,
            static_url_path='',
            static_folder='templates')

app.secret_key = os.getenv('Flask_SESSION.SECRET_KEY')
app.permanent_session_lifetime = timedelta(hours=1)


@app.route("/", methods=['GET'])
def index():
    cart_items_number = 0
    if 'cart_items' in session:
        for item in session['cart_items']:
            cart_items_number += item["quantity"]

    products = products_get_data()
    for product in products:
        product["Amount"] = currency_formatter(
            product["Amount"], product["Currency"])
    return render_template('index.html', products=products, cart_items_number=cart_items_number)

"""
@app.route("/complete-registration", methods=['POST'])
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
"""

@app.route("/cart/<product_id>", methods=['POST'])
def add_to_cart(product_id):
    product = get_item_by_productID(product_id)[0]
    session.permanent = True

    if 'cart_items' not in session:
        session['cart_items'] = []
    cart_list = session['cart_items']
    # cart_list = [{"id": productID, "quantity": int}, ...]

    index_in_cart = get_items_in_cart(cart_list, product["id"])
    if index_in_cart is not None:
        cart_list[index_in_cart]["quantity"] += 1
    else:
        cart_list.append({"id": product["id"], 'quantity': 1})
    session['cart_items'] = cart_list
    return redirect("/")


@app.route("/delete/<product_id>", methods=['POST'])
def delete_from_cart(product_id):
    if 'cart_items' not in session:
        return redirect("/")
    cart_list = session['cart_items']
    for item in cart_list:
        if product_id in item["id"]:
            cart_list.remove(item)
    print(cart_list)
    session['cart_items'] = cart_list
    return redirect("/checkout")


def get_items_in_cart(list, id):
    return next((i for i, x in enumerate(list) if x["id"] == id), None)


@app.route("/checkout", methods=['GET', 'POST'])
def checkout():
    if "cart_items" not in session:
        return redirect("/")
    items = session['cart_items']
    checkout_items = []
    try:
        for item in items:
            product = get_item_by_productID(item["id"])[0]
            product["quantity"] = item["quantity"]
            product["value"] = item["quantity"] * product["Amount"]
            if isinstance(product["Amount"], int):
                product["Amount"] = currency_formatter(
                    product["Amount"], product["Currency"])
                product["value"] = currency_formatter(
                    product["value"], product["Currency"])
            checkout_items.append(product)
    except Exception as e:
        print(e)
    return render_template('checkout.html', items=checkout_items)


@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    if 'cart_items' not in session:
        redirect("/")
    try:
        items = []
        cart_items = session['cart_items']
        for item in cart_items:
            print(item)
            product = get_item_by_productID(item["id"])[0]
            print(product)
            items.append(
                {'price': product["Price ID"], 'quantity': item['quantity'], })
        checkout_session = stripe.checkout.Session.create(
            line_items=items,
            mode='payment',
            success_url= YOUR_DOMAIN + '/success.html',
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
    price = "{}  {:,.2f}".format(curr, value)
    return price


if __name__ == '__main__':
    app.run(port=4242)
