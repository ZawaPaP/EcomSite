from flask import Flask, render_template, request, redirect, url_for
import hashlib
import json
import stripe

# This is your test secret API key.
stripe.api_key = 'sk_test_51MZbIFA9Qashsbv2iR7UnyIYHgP78XhB1gZRqZQ8mozqCCGabK47D3MnIyEzhUiABXvX73CZ2nJZRMbJwgqBYJGE00Cgi5aOoP'
YOUR_DOMAIN = 'http://localhost:4242'


app = Flask(__name__, 
            static_url_path='',
            static_folder='templates')

@app.route("/", methods = ['GET', 'POST'])
def index():
    if request.method == "POST":
        data = request.form["data"]
        return redirect (url_for("checkout", data=data))
    return render_template('index.html')


@app.route("/checkout", methods = ['GET', 'POST'])
def checkout():
    item = json.loads(request.form.get('select_item'))
    return render_template('checkout.html', item = item)

@app.route("/thanks", methods = ['POST'])
def thanks():
    fn = request.form.get('firstName')
    ln = request.form.get('lastName')
    em = request.form.get('email')
    ph = request.form.get('phone')
    address = request.form.get('address')
    address2 = request.form.get('address2')
    data = {
        'fn': fn, 
        'ln': ln,
        'em': em, 
        'ph': ph, 
        'address': address,
        'address2': address2
    }
    hash_data = {
        'fn': hash(fn), 
        'ln': hash(ln),
        'em': hash(em), 
        'ph': hash(ph), 
        'address': hash(address),
        'address2': hash(address2)  
    }
        
    return render_template('thanks.html', data = data, hash_data = hash_data)


@app.route("/success")
def success():
    return render_template('success.html')

@app.route("/cancel")
def cancel():
    return render_template('cancel.html')


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

def hash(string):
    return hashlib.sha256(string.encode('utf-8')).hexdigest()

if __name__ == '__main__':
    app.run(port=4242)