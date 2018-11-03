import os
from PIL import Image
from flask import url_for, render_template, flash, redirect, request
from FlaskSite import app, bcrypt, db
from FlaskSite.Forms import RegistrationForm, LoginForm, EditProfileForm
from FlaskSite.Models import User
from flask_login import login_user, current_user, logout_user, login_required

title = 'VT Shop'
customerImagePath = 'Database/Pictures/User/'
itemImagePath = 'Database/Pictures/Item/'

@app.route('/')
@app.route('/home')
def Home():
    return render_template('index.html', title=title+' - Index')

@app.route('/about')
def About():
    return render_template('about.html', title=title+' - About')

@app.route('/cart')
def Cart():
    return render_template('cart.html', title=title+' - Cart')

@app.route('/add_item')
def AddItem():
    if current_user.is_authenticated and current_user.permission == 0:
        return render_template('addItem.html', title=title+' - Add Item')
    return redirect(url_for('Home'))

@app.route('/view_users')
def ViewUser():
    if current_user.is_authenticated and current_user.permission == 0:
            return render_template('viewUser.html', title=title+' - View User')
    return redirect(url_for('Home'))

@app.route('/transaction')
def Transaction():
    return render_template('transaction.html', title=title+' - Transaction')

@app.route('/history')
def History():
    return render_template('history.html', title=title+' - History')

@app.route('/register', methods=['GET', 'POST'])
def Register():
    if current_user.is_authenticated:
        return redirect(url_for('Home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashedPassword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(firstName = form.firstName.data, lastName = form.lastName.data, username = form.username.data, email = form.email.data, password = hashedPassword, address = form.address.data, phone = form.phone.data, bank = form.bank.data)
        db.session.add(user)
        db.session.commit()
        flash('Account Created', 'success')
        return redirect(url_for('Login'))
    return render_template('register.html', title=title+' - Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def Login():
    if current_user.is_authenticated:
        return redirect(url_for('Home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if not user:
            user = User.query.filter_by(username = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            flash('You have been logged in!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('Home'))
        flash('Wrong email or password!', 'danger')
    return render_template('login.html', title=title+' - Login', form=form)

@app.route('/logout')
def Logout():
    logout_user()
    flash('You have been logged out!', 'success')
    return redirect(url_for('Login'))

def SaveUserPicture(form_picture):
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_name = current_user.username + f_ext
    picture_path = os.path.join(app.root_path, 'static/'+customerImagePath, picture_name)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_name

@app.route('/account', methods=['GET', 'POST'])
@login_required
def Account():
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
        return redirect(url_for('Account'))
    elif request.method == 'GET':
        form.firstName.data = current_user.firstName
        form.lastName.data = current_user.lastName
        form.email.data = current_user.email
        form.address.data = current_user.address
        form.phone.data = current_user.phone
        form.bank.data = current_user.bank
    user_image = url_for('static', filename = customerImagePath+current_user.image_file)
    return render_template('editProfile.html', title=title+' - Account', user_image=user_image, form=form)

# @app.errorhandler(404)
# def page_not_found(e):
#     # note that we set the 404 status explicitly
#     return render_template('error.html'), 404

if __name__ == '__main__':
    app.run(debug=True)