from app import app,db
from models import User

with app.app_context():
    db.create_all()
    user = User(username='xyz1')
    user.set_password('xyz1')
    db.session.add(user)
    db.session.commit()