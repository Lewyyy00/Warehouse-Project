from flask import Flask, render_template, request
from magazyn2 import items
from forms import AddNewProductForm
from magazyn2 import Product
app = Flask(__name__)
app.config['SECRET_KEY'] = 'sekretnykod'

@app.route('/', methods = ["GET", "POST"])
def index():
    list_of_products = items
    form = AddNewProductForm()
    if request.method == "POST":
        new_product = Product(form.name.data,form.quantity.data,form.unit.data,form.unit_price.data)
        items[f'product_{len(items)+1}'] = new_product
    return render_template('products_list.html', list_of_products = list_of_products, form=form)

