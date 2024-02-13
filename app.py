from flask import Flask, render_template, request, Response
from magazyn2 import items
from forms import AddNewProductForm
from magazyn2 import Product
import csv
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

@app.route("/export_to_csv")
def export_to_csv():
    with open('magazyn.csv', 'w', newline='') as csvfile:
        fieldnames = ["name","quantity","unit","unit_price"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item_key in items:
            item = vars(items[item_key])    
            writer.writerow(item)
    return Response("Dane zostały wyeksportowane do pliku CSV.", status=200, mimetype='text/plain')
