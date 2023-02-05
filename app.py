from flask import Flask, render_template, request, redirect, url_for
import hashlib

app = Flask(__name__, static_folder='./templates/images')

@app.route("/", methods = ['GET', 'POST'])
def index():
    if request.method == "POST":
        data = request.form["data"]
        print(data)
        return redirect (url_for("checkout", data=data))
    return render_template('index.html')


@app.route("/checkout", methods = ['GET', 'POST'])
def checkout():
    item = request.form.get('select_item')
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

def hash(string):
    return hashlib.sha256(string.encode('utf-8')).hexdigest()