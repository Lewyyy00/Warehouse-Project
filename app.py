from flask import Flask, render_template, request, Response, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user
from src.forms import *
from src.magazyn import *
import csv
import sqlite3

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sekretnykod'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///magazyn.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

con = sqlite3.connect("magazyn.db")

users = {1: User(id=1, username='xyz', password_hash=bcrypt.generate_password_hash('xyz').decode('utf-8'))}

@login_manager.user_loader
def load_user(user_id):
    user = users.get(user_id)
    return user

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = next((u for u in users.values() if u.username == username), None)
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_2 = request.form['password_2']

        if password == password_2:
            password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
            user_id = len(users) + 1
            users[user_id] = User(id=user_id, username=username, password_hash=password_hash)
            flash('User registered successfully!')
            return redirect(url_for('login'))
        else:
            flash('passwords are not the same')

    return render_template('register.html')

@app.route('/dashboard', methods=["GET", "POST"])
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