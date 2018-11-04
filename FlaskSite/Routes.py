import os
from PIL import Image
from flask import url_for, render_template, flash, redirect, request
from FlaskSite import app, bcrypt, db
from FlaskSite.Forms import RegistrationForm, LoginForm, EditProfileForm, AddItemForm, AddCategoryForm, ChangePasswordForm
from FlaskSite.Models import User, Item, Category, CartDetail, Cart, Transaction, TransactionDetail, History, HistoryDetail, Status, Category
from flask_login import login_user, current_user, logout_user, login_required

title = 'VT Shop'
customerImagePath = 'Database/Pictures/User/'
itemImagePath = 'Database/Pictures/Item/'

@app.route('/')
@app.route('/home')
@app.route('/index')
def Home():
    items = Item.query.order_by(Item.price.desc())
    # page = request.args.get('page', 1, type=int)
    # items = Item.query.order_by(Item.price).paginate(page=page, per_page=2)
    return render_template('index.html', title=title+' - Index', items=items)

@app.route("/item/<int:item_id>")
def ViewItem(item_id):
    item = Item.query.get(item_id)
    return render_template('item.html', title=title+' - '+item.name, item=item)

@app.route("/category/<int:category_id>")
def ViewCategory(category_id):
    category = Category.query.get(category_id)
    items = Item.query.filter_by(category_id=category_id).all()
    return render_template('category.html', title=title+' - '+category.name, category=category, items=items)

@app.route('/about')
def About():
    return render_template('about.html', title=title+' - About')

@app.route('/cart')
@login_required
def UserCart():
    return render_template('cart.html', title=title+' - Cart')

def SaveItemPicture(form_picture):
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_name = current_user.username + f_ext
    picture_path = os.path.join(app.root_path, 'static/'+customerImagePath, picture_name)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_name

@app.route('/add_item', methods=['GET', 'POST'])
@login_required
def AddItem():
    if not current_user.is_authenticated or current_user.permission == 1:
        return redirect(url_for('Home'))
    categories = Category.query.all() 
    form = AddItemForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = SaveUserPicture(form.picture.data)
            current_user.image_file = picture_file
        print("Test")
        print(form.category_id.data)
        item = Item(name = form.name.data, price = form.price.data, unit=form.unit.data, description = form.description.data, category_id = form.category_id.data, stock = form.stock.data)
        db.session.add(item)
        db.session.commit()
        flash('Item Added!', 'success')
        return redirect(url_for('AddItem'))
    return render_template('addItem.html', title=title+' - Add Item', form=form, categories=categories)

@app.route('/add_category', methods=['GET', 'POST'])
@login_required
def AddCategory():
    if not current_user.is_authenticated or current_user.permission == 1:
        return redirect(url_for('Home'))
    form = AddCategoryForm()
    if form.validate_on_submit():
        category = Category(name = form.name.data, description = form.description.data)
        db.session.add(category)
        db.session.commit()
        flash('Category Added!', 'success')
        return redirect(url_for('AddCategory'))
    return render_template('addCategory.html', title=title+' - Add Category', form=form)

@app.route('/view_users')
@login_required
def ViewUser():
    users = User.query.all()
    if not current_user.is_authenticated or current_user.permission == 1:
        return redirect(url_for('Home'))
    
    return render_template('viewUser.html', title=title+' - View User', users=users)

@app.route('/transaction')
@login_required
def AllTransaction():
    return render_template('transaction.html', title=title+' - Transaction')

@app.route('/history')
@login_required
def AllHistory():
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
@login_required
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

@app.route('/account')
@login_required
def Account():
    return render_template('account.html', title=title+' Account')

@app.route('/edit_profile', methods=['GET', 'POST'])
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
        return redirect(url_for('Account'))
    elif request.method == 'GET':
        form.firstName.data = current_user.firstName
        form.lastName.data = current_user.lastName
        form.email.data = current_user.email
        form.address.data = current_user.address
        form.phone.data = current_user.phone
        form.bank.data = current_user.bank
    user_image = url_for('static', filename = customerImagePath+current_user.image_file)
    return render_template('editProfile.html', title=title+' - Edit Profile', user_image=user_image, form=form)


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def ChangePassword():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.oldPassword.data):
            current_user.password = bcrypt.generate_password_hash(form.newPassword.data).decode('utf-8')
            db.session.commit()
            flash('Your account password has been updated!', 'success')
            return redirect(url_for('Account'))
        else:
            flash('Wrong password', 'danger')
    user_image = url_for('static', filename = customerImagePath+current_user.image_file)
    return render_template('changePassword.html', title=title+' - Change Password', user_image=user_image, form=form)

# @app.errorhandler(404)
# def page_not_found(e):
#     # note that we set the 404 status explicitly
#     return render_template('error.html'), 404

if __name__ == '__main__':
    app.run(debug=True)