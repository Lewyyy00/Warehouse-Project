from flask import Flask, render_template
from magazyn2 import items
app = Flask(__name__)

@app.route('/', methods = ["GET"])
def index():
    list_of_products = items
    return render_template('products_list.html', list_of_products = list_of_products)

