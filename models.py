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


class DatabaseOperations:


    def add_new_user(user, email, passoword):
        
        new_user = User(
            
            username = user,
            email = email,
            password_hash = passoword

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

    def remove_user(user_id):

        user = User.query.get(user_id)

        try:
            db.session.delete(user)
            db.session.commit()
            print(f"USER: {user_id} was deleted!")

        except Exception as e:
            db.session.rollback()
            print(f"ERROR: {e}")

        finally:
            db.session.close()  
            
def add_record(model, **kwargs):

    """
    A method, that adds new record of data in table.
    
    Args:
        model (db.Model): User, Product, Category etc.
        **kwargs: key-value data like username="John".
    
    Returns:
        record or none if error.
    """
    try:
        record = model(**kwargs)
        db.session.add(record)
        db.session.commit()
        print(f"record was added in {model.__tablename__}: {record}")
        return record

    except Exception as e:
        db.session.rollback()
        print(f"ERROR: {e}")
        return None

    finally:
        db.session.close()  



    """def add_new_product(name, category_id, description, unit, unit_price):

        new_product = Product(
            
            name = name,
            description = description,
            category_id = category_id,
            unit = unit,
            unit_price = unit_price

            )
        
        user_product = UserProduct(user_id=new_user.id, product_id=new_product.id, quantity=2)
        db.session.add(user_product)
        
        db.session.add(new_product)

        try:
            db.session.commit()
            print(f"USER: {new_product.name} was added!")

        except Exception as e:
            db.session.rollback()
            print(f"ERROR: {e}")

        finally:
            db.session.close()  

    def remove_new_product(name, description, unit, unit_price):

        new_product = Product(
        
            name=f"{name}",
            description=f"{description}",
            unit=f"{unit}",
            unit_price=f"{unit_price}"

            )
        
    
        db.session.add(new_product)

        try:
            db.session.commit()
            print(f"USER: {new_product.name} was added!")

        except Exception as e:
            db.session.rollback()
            print(f"ERROR: {e}")

        finally:
            db.session.close()  """



