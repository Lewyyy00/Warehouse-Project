from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired

class AddNewProductForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    quantity = IntegerField("quantity", validators=[DataRequired()])
    unit = StringField('unit', validators=[DataRequired()])
    unit_price = StringField('unit_price', validators=[DataRequired()])
