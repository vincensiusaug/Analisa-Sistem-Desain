from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from FlaskSite.Models import  User, Category

allowedPictureExt = ['png', 'jpg', 'jpeg']

class TransactionForm(FlaskForm):
    status = SelectField('Status', choices=[], coerce=int, validators=[DataRequired()])
    submit = SubmitField('Change')