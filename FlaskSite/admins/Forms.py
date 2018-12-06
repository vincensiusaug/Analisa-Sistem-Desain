from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from FlaskSite.Models import  User, Category

class ChangeUserTypeForm(FlaskForm):
    userType = SelectField('User Type', choices=[], coerce=int, validators=[DataRequired()])
    submit = SubmitField('Save')