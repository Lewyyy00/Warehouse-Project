from flask import Flask, render_template, request, Response, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required
from src.forms import *
from src.magazyn import *
import csv
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

from db_instance import db 
db.init_app(app)  
migrate = Migrate(app, db)

from operations import DatabaseOperations
from models import User, UserProduct, Product, Category

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user:
            print(f"Stored hash: {user.password_hash}")
            print(f"Entered password: {password}")
            print(f"Password match: {bcrypt.check_password_hash(user.password_hash, password)}")

        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            flash('You have been logged in')
            return redirect(url_for('index'))
        
        else:
            flash('Invalid username or password')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':    
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password_2 = request.form['password_2']

        if password == password_2:
            existing_user = User.query.filter_by(username=username).first() #check if user with this username exists 
            if existing_user:
                flash('Username already taken. Please choose another one.')
                return redirect(url_for('register'))
            else:
        
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                DatabaseOperations.add_new_user(username, email, hashed_password)
                flash('Registration successful. You can now log in.')
                return redirect(url_for('login'))
                
        else:
            flash('passwords are not the same')
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/main', methods=["GET", "POST"])
@login_required
def index():
    list_of_products = Product.query.all()
    form = AddNewProductForm()
    
    if request.method == "POST":

        if "changed_quantity" in request.form and "product_id" in request.form:
            product_id = int(request.form["product_id"])
            changed_quantity = int(request.form["changed_quantity"])
            
            product = Product.query.get(product_id)
            if product and product.quantity + changed_quantity >= 0:
                product.quantity += changed_quantity
                db.session.commit()
                flash("Quantity updated successfully!", "success")
            else:
                flash("Error: Insufficient stock or invalid product.", "danger")
        else:
            if form.validate_on_submit():
                new_product = Product(
                    name=form.name.data,
                    description=form.description.data,
                    unit=form.unit.data,
                    unit_price=form.unit_price.data,
                    quantity=form.quantity.data
                )
                db.session.add(new_product)
                db.session.commit()
                flash("New product added successfully!", "success")
            else:
                flash("Error: Invalid form submission.", "danger")

    return render_template('products_list.html', list_of_products=list_of_products, form=form)

"""@app.route('/delete_product/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        flash('Product deleted successfully!', 'success')
    else:
        flash('Product not found.', 'danger')
    return redirect(url_for('index'))

@app.route('/add_product', methods=['POST'])
@login_required
def add_product():
    form = AddNewProductForm()
    if form.validate_on_submit():
        new_product = Product(
            name=form.name.data,
            description=form.description.data,
            unit=form.unit.data,
            unit_price=form.unit_price.data,
            quantity=form.quantity.data
        )
        db.session.add(new_product)
        db.session.commit()
        flash('New product added successfully!', 'success')
    else:
        flash('Error: Invalid form submission.', 'danger')
    return redirect(url_for('index'))"""

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


@app.route ("/admin", methods=["GET", "POST"])
def admin():
    pass


if __name__ == '__main__':
    app.run(debug=True)

