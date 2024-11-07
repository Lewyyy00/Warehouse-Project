from flask import Flask, render_template, request, Response, redirect, url_for
from magazyn import items, Product
from forms import AddNewProductForm
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sekretnykod'

@app.route('/', methods=["GET", "POST"])
def index():
    list_of_products = items
    form = AddNewProductForm()
    
    if request.method == "POST":
        if "sell_quantity" in request.form and "product_id" in request.form:
            product_id = request.form["product_id"]
            sell_quantity = int(request.form["sell_quantity"])
            
            if product_id in items and items[product_id].quantity >= sell_quantity:
                items[product_id].quantity -= sell_quantity
        else:
            
            new_product = Product(form.name.data, form.quantity.data, form.unit.data, form.unit_price.data)
            items[f'product_{len(items) + 1}'] = new_product

    return render_template('products_list.html', list_of_products=list_of_products, form=form)


@app.route("/export_to_csv")
def export_to_csv():
    with open('magazyn.csv', 'w', newline='') as csvfile:
        fieldnames = ["name","quantity","unit","unit_price"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item_key in items:
            item = vars(items[item_key])    
            writer.writerow(item)
    return redirect(url_for("index"))

@app.route("/import_from_csv")
def import_from_csv():
    items.clear()

    with open('magazyn.csv', newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for i, row in enumerate(csv_reader):
            product_name = row["name"]
            product = Product(product_name, int(row["quantity"]), row["unit"], float(row["unit_price"]))
            items[f'product_{i+1}'] = product

    return redirect(url_for("index"))


@app.route('/sell/<product_name>', methods=["GET", "POST"])
def sell_product():
    pass

if __name__ == '__main__':
    app.run(debug=True)