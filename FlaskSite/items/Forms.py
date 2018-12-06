from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from FlaskSite.Models import  Item
from FlaskSite.Variables import *

class AddItemForm(FlaskForm):
    name = StringField('Item Name', validators=[DataRequired(), Length(min=2, max=40)])
    price = IntegerField('Price', validators=[DataRequired()])
    unit = StringField('Unit', validators=[DataRequired(), Length(min=1, max=20)])
    description = StringField('Description', validators=[DataRequired(), Length(min=2, max=200)])
    category_id = SelectField('Category', choices=[], coerce=int, validators=[DataRequired()])
    stock = IntegerField('Stock', validators=[DataRequired()])
    picture = FileField('Upload Item Picture', validators=[FileAllowed(allowedPictureExt)])
    submit = SubmitField('Add')

    def validate_name(self, name):
        item = Item.query.filter_by(name = name.data).first()
        if item:
            raise ValidationError('This name is exist.')

class EditItemForm(FlaskForm):
    name = StringField('Item Name', validators=[DataRequired(), Length(min=2, max=40)])
    price = IntegerField('Price', validators=[DataRequired()])
    unit = StringField('Unit', validators=[DataRequired(), Length(min=1, max=20)])
    description = StringField('Description', validators=[DataRequired(), Length(min=2, max=200)])
    category_id = SelectField('Category', choices=[], coerce=int, validators=[DataRequired()])
    stock = IntegerField('Stock', validators=[DataRequired()])
    picture = FileField('Change Item Picture', validators=[FileAllowed(allowedPictureExt)])
    submit = SubmitField('Edit')

    def validate_name(self, name):
        item = Item.query.filter_by(name = name.data).first()
        if item:
            raise ValidationError('This name is exist.')

class AddCartForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Add to cart')