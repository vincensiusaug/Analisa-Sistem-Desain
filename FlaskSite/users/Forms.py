from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from FlaskSite.Models import  User
from FlaskSite.Variables import *

class RegistrationForm(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    lastName = StringField('Last Name', validators=[Length(min=0, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    address = StringField('Address', validators=[DataRequired(), Length(min=2, max=60)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=8, max=20)])
    bank = StringField('Bank Number', validators=[DataRequired(), Length(min=8, max=20)])
    submit = SubmitField('Register')

    def validate_bank(self, bank):
        try:
            int(bank.data)
        except:
            raise ValidationError('Invalid bank number.')
    
    def validate_phone(self, phone):
        try:
            int(phone.data)
        except:
            raise ValidationError('Invalid phone number11.'+phone)

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('This username is taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('This email is taken.')

class LoginForm(FlaskForm):
    email = StringField('Username or Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class EditProfileForm(FlaskForm):
    picture = FileField('Upload Profile Picture', validators=[FileAllowed(allowedPictureExt)])
    firstName = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    lastName = StringField('Last Name', validators=[Length(min=0, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[DataRequired(), Length(min=2, max=60)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=8, max=20)])
    bank = StringField('Bank Number', validators=[DataRequired(), Length(min=8, max=20)])
    submit = SubmitField('Update')
    
    def validate_bank(self, bank):
        try:
            int(bank.data)
        except:
            raise ValidationError('Invalid bank number.')
    
    def validate_phone(self, phone):
        try:
            int(phone.data)
        except:
            raise ValidationError('Invalid phone number.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('This email is taken.')

class ChangePasswordForm(FlaskForm):
    oldPassword = PasswordField('Old password', validators=[DataRequired(), Length(min=8, max=20)])
    newPassword = PasswordField('New Password', validators=[DataRequired()])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('newPassword')])
    submit = SubmitField('Change')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirmPassword = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')