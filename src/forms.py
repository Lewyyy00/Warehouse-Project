from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length
from flask_login import UserMixin

class AddNewProductForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    description = StringField("Description", validators=[Length(max=500)])
    quantity = IntegerField("quantity", validators=[DataRequired()])
    unit = StringField('unit', validators=[DataRequired()])
    unit_price = StringField('unit_price', validators=[DataRequired()])

