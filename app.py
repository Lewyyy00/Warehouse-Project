from flask import Flask, render_template, request, Response, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, UserMixin
from src.forms import *
from src.magazyn import *
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sekretnykod'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, username, password_hash, role='user'):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.role = role

users = {1: User(id=1, username='xyz', password_hash=bcrypt.generate_password_hash('xyz').decode('utf-8'))}

@login_manager.user_loader
def load_user(user_id):
    user = users.get(user_id)
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(users.values)
        user = next((u for u in users.values() if u.username == username), None)
        print(user)
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/', methods=["GET", "POST"])
def index():
    list_of_products = items
    form = AddNewProductForm()
    
    if request.method == "POST":
        if "changed_quantity" in request.form and "product_id" in request.form:
            product_id = request.form["product_id"]
            changed_quantity = int(request.form["changed_quantity"])
            
            if product_id in items and items[product_id].quantity >= changed_quantity:
                items[product_id].quantity += changed_quantity
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