from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from FlaskSite.Models import  User

class RegistrationForm(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    lastName = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    address = StringField('Address', validators=[DataRequired(), Length(min=2, max=20)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=8, max=20)])
    bank = StringField('Bank Number', validators=[DataRequired(), Length(min=8, max=20)])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('This username is taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('This email is taken.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UserForm(FlaskForm):
    home = SubmitField('Home')