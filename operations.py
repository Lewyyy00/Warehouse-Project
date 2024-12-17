from models import User, Product, Category, UserProduct
from db_instance import db

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

    def remove_product(id):

        product = Product.query.get(id)

        try:
            db.session.delete(product)
            db.session.commit()
            print(f"USER: {product} was deleted!")

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

        existing_record = model.query.filter_by(**kwargs).first()
        if existing_record:
            print(f"Record already exists in {model.__tablename__}: {existing_record}")
            return existing_record

        record = model(**kwargs)
        db.session.add(record)
        db.session.flush()
        print(f"record was added in {model.__tablename__}: {record}")
        return record

    except Exception as e:
        db.session.rollback()
        print(f"ERROR: {e}")
        return None

def add_data(cat_name, prod_name, prod_desc, prod_unit, prod_unit_price, quantity, userid):
    try:
        
        with db.session.begin():
            category = add_record(
                Category, 
                name=cat_name
                )
            
            if not category:
                raise ValueError('Error when adding category')
            
            product = add_record(
                Product, 
                name=prod_name, 
                description=prod_desc, 
                category_id=category.id, 
                unit=prod_unit, 
                unit_price=prod_unit_price
                )
            
            if not product:
                raise ValueError('Error when adding product')
            
            user_product = add_record(
                UserProduct, 
                user_id=userid, 
                product_id=product.id, 
                quantity=quantity
                )
            
            if not user_product:
                raise ValueError('Error when adding user_product')
            
            print(f"the {category}, {product}, {user_product} were added")

    except Exception as e:
        db.session.rollback()
        print(f"ERROR: {e}")


"""with app.app_context():
    
    add_data(
        cat_name="Electronics",
        prod_name="Laptop",
        prod_desc="Latest model with AI features",
        prod_unit="pcs",
        prod_unit_price=1799.99,
        quantity=100,
        userid=1
        )
"""