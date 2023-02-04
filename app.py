from flask import Flask, render_template, request, redirect, url_for

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
    return render_template('checkout.html')

@app.route("/thanks")
def thanks():
    return render_template('thanks.html')
