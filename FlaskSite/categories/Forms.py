from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from FlaskSite.Models import  User, Category
from FlaskSite.Variables import *

class AddCategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired(), Length(min=2, max=40)])
    description = StringField('Description', validators=[DataRequired(), Length(min=2, max=200)])
    submit = SubmitField('Add')

    def validate_name(self, name):
        category = Category.query.filter_by(name = name.data).first()
        if category:
            raise ValidationError('This name is exist.')

class EditCategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired(), Length(min=2, max=40)])
    description = StringField('Description', validators=[DataRequired(), Length(min=2, max=200)])
    submit = SubmitField('Edit')

    def validate_name(self, name):
        category = Category.query.filter_by(name = name.data).first()
        if category:
            raise ValidationError('This name is exist.')
