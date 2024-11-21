from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired
from flask_login import UserMixin

class AddNewProductForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    quantity = IntegerField("quantity", validators=[DataRequired()])
    unit = StringField('unit', validators=[DataRequired()])
    unit_price = StringField('unit_price', validators=[DataRequired()])

class User(UserMixin):
    def __init__(self, id, username, password_hash, role='user'):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.role = role

