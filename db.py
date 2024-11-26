from app import app,db
from models import User

with app.app_context():
    db.create_all()
    user = User(username='admin')
    user.set_password('admin123')
    db.session.add(user)
    db.session.commit()