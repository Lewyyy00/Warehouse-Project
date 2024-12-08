from app import *


class User(UserMixin, db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    products = db.relationship('UserProduct', back_populates='user', lazy=True)
 
class UserProduct(db.Model):

    __tablename__ = "user_products"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', back_populates='products')
    product = db.relationship('Product', back_populates='user_products')

class Product(db.Model):

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    unit = db.Column(db.String(50), nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    user_products = db.relationship('UserProduct', back_populates='product', lazy=True)

class Category(db.Model):

    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    products = db.relationship('Product', backref='category', lazy=True)

def add_new_user(user, email, passoword):
    
    new_user = User(
        
        username=f"{user}",
        email=f"{email}",
        password_hash=f"{passoword}"

        )
    
    db.session.add(new_user)

    try:
        db.session.commit()
        print(f"USER: {new_user.username} was added!")

    except Exception as e:
        db.session.rollback()
        print(f"ERROR: {e}")

    finally:
        db.session.close()  