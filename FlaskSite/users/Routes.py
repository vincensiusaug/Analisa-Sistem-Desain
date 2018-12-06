import os
from sqlalchemy import or_
from PIL import Image
from flask import url_for, render_template, flash, redirect, request, abort, Blueprint
from FlaskSite import app, bcrypt, db, mail
from FlaskSite.users.Forms import (RegistrationForm,  LoginForm, EditProfileForm, ChangePasswordForm, RequestResetForm,
                                    ResetPasswordForm)
from FlaskSite.Models import (UserType, User, Item, Category, Cart, Transaction, TransactionDetail, History, HistoryDetail,
                            Status, Category, Chat, ChatDetail, ShippingRecord, Shipping)
from flask_login import login_user, current_user, logout_user, login_required

from FlaskSite.users.Utils import SaveUserPicture, SendResetEmail

users = Blueprint('users', __name__)
title = 'VT Shop'
userImagePath = 'Database/Pictures/User/'
itemImagePath = 'Database/Pictures/Item/'
perPageItem = 5
perPageUser = 5
restrictedUser = ("Customer")
specialUser = ("Owner", "Admin")

@users.route('/register', methods=['GET', 'POST'])
def Register():
    if current_user.is_authenticated:
        return redirect(url_for('main.Home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashedPassword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(firstName = form.firstName.data, lastName = form.lastName.data, username = form.username.data, email = form.email.data, password = hashedPassword, address = form.address.data, phone = form.phone.data, bank = form.bank.data)
        db.session.add(user)
        db.session.commit()
        flash('Account Created', 'success')
        return redirect(url_for('users.Login'))
    return render_template('register.html', title=title+' - Register', form=form)

@users.route('/login', methods=['GET', 'POST'])
def Login():
    if current_user.is_authenticated:
        return redirect(url_for('main.Home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if not user:
            user = User.query.filter_by(username = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            flash('You have been logged in!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.Home'))
        flash('Wrong email or password!', 'danger')
    return render_template('login.html', title=title+' - Login', form=form)

@users.route('/logout')
@login_required
def Logout():
    logout_user()
    flash('You have been logged out!', 'success')
    return redirect(url_for('users.Login'))

@users.route('/account')
@login_required
def Account():
    return render_template('userInfo.html', title=title+' Account')

@users.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def EditProfile():
    form = EditProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = SaveUserPicture(form.picture.data)
            current_user.image_file = picture_file
        current_user.firstName = form.firstName.data
        current_user.lastName = form.lastName.data
        current_user.email = form.email.data
        current_user.address = form.address.data
        current_user.phone = form.phone.data
        current_user.bank = form.bank.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.Account'))
    elif request.method == 'GET':
        form.firstName.data = current_user.firstName
        form.lastName.data = current_user.lastName
        form.email.data = current_user.email
        form.address.data = current_user.address
        form.phone.data = current_user.phone
        form.bank.data = current_user.bank
    user_image = url_for('static', filename = userImagePath+current_user.image_file)
    return render_template('editProfile.html', title=title+' - Edit Profile', user_image=user_image, form=form)


@users.route('/change_password', methods=['GET', 'POST'])
@login_required
def ChangePassword():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.oldPassword.data):
            current_user.password = bcrypt.generate_password_hash(form.newPassword.data).decode('utf-8')
            db.session.commit()
            flash('Your account password has been updated!', 'success')
            return redirect(url_for('users.Account'))
        else:
            flash('Wrong password', 'danger')
    user_image = url_for('static', filename = userImagePath+current_user.image_file)
    return render_template('changePassword.html', title=title+' - Change Password', user_image=user_image, form=form)

@users.route("/reset_password", methods=['GET', 'POST'])
def ResetRequest():
    if current_user.is_authenticated:
        return redirect(url_for('main.Home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        SendResetEmail(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.Login'))
    return render_template('resetRequest.html', title='Reset Password', form=form)

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def ResetToken(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.Home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.ResetRequest'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.Login'))
    return render_template('resetToken.html', title='Reset Password', form=form)