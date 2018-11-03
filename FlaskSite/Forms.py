from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from FlaskSite.Models import  User

allowedPictureExt = ['png', 'jpg', 'jpeg']

class RegistrationForm(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    lastName = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    address = StringField('Address', validators=[DataRequired(), Length(min=2, max=60)])
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
    # email = StringField('Email', validators=[DataRequired(), Email()])
    email = StringField('Username or Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class AddItemForm(FlaskForm):
    # email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Item Name', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    stock = IntegerField('Stock', validators=[DataRequired()])
    picture = FileField('Upload Item Picture', validators=[FileAllowed(allowedPictureExt)])
    submit = SubmitField('Add')

class EditProfileForm(FlaskForm):
    picture = FileField('Upload Profile Picture', validators=[FileAllowed(allowedPictureExt)])
    firstName = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    lastName = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[DataRequired(), Length(min=2, max=60)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=8, max=20)])
    bank = StringField('Bank Number', validators=[DataRequired(), Length(min=8, max=20)])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('This email is taken.')

