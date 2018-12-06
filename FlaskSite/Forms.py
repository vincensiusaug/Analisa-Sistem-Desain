from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from FlaskSite.Models import  User, Category

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
    email = StringField('Username or Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class AddItemForm(FlaskForm):
    name = StringField('Item Name', validators=[DataRequired(), Length(min=2, max=40)])
    price = IntegerField('Price', validators=[DataRequired()])
    unit = StringField('Unit', validators=[DataRequired(), Length(min=1, max=20)])
    description = StringField('Description', validators=[DataRequired(), Length(min=2, max=200)])
    category_id = SelectField('Category', choices=[], coerce=int, validators=[DataRequired()])
    stock = IntegerField('Stock', validators=[DataRequired()])
    picture = FileField('Upload Item Picture', validators=[FileAllowed(allowedPictureExt)])
    submit = SubmitField('Add')

class EditItemForm(FlaskForm):
    name = StringField('Item Name', validators=[DataRequired(), Length(min=2, max=40)])
    price = IntegerField('Price', validators=[DataRequired()])
    unit = StringField('Unit', validators=[DataRequired(), Length(min=1, max=20)])
    description = StringField('Description', validators=[DataRequired(), Length(min=2, max=200)])
    category_id = SelectField('Category', choices=[], coerce=int, validators=[DataRequired()])
    stock = IntegerField('Stock', validators=[DataRequired()])
    picture = FileField('Change Item Picture', validators=[FileAllowed(allowedPictureExt)])
    submit = SubmitField('Edit')

class AddCategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired(), Length(min=2, max=40)])
    description = StringField('Description', validators=[DataRequired(), Length(min=2, max=200)])
    submit = SubmitField('Add')

class EditCategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired(), Length(min=2, max=40)])
    description = StringField('Description', validators=[DataRequired(), Length(min=2, max=200)])
    submit = SubmitField('Edit')

class EditProfileForm(FlaskForm):
    picture = FileField('Upload Profile Picture', validators=[FileAllowed(allowedPictureExt)])
    firstName = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    lastName = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[DataRequired(), Length(min=2, max=60)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=8, max=20)])
    bank = IntegerField('Bank Number', validators=[DataRequired(), Length(min=8, max=20)])
    submit = SubmitField('Update')

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

class AddCartForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Add to cart')

class ChangeUserTypeForm(FlaskForm):
    userType = SelectField('User Type', choices=[], coerce=int, validators=[DataRequired()])
    submit = SubmitField('Save')

class ChatForm(FlaskForm):
    text = StringField('Text', validators=[DataRequired()])
    submit = SubmitField('Send')

class TransactionForm(FlaskForm):
    status = SelectField('Status', choices=[], coerce=int, validators=[DataRequired()])
    submit = SubmitField('Change')
