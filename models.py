from app import db
class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True, unique=True)
    email = db.Column(db.String(200), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __str__(self):
        return f"<User {self.username}>"

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