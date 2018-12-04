import os
from sqlalchemy import or_
from PIL import Image
from flask import url_for, render_template, flash, redirect, request, abort
from FlaskSite import app, bcrypt, db
from FlaskSite.Forms import RegistrationForm, AddItemForm, LoginForm, EditProfileForm, AddCategoryForm, ChangePasswordForm, AddCartForm, ChangeUserTypeForm, ChatForm
from FlaskSite.Models import UserType, User, Item, Category, Cart, Transaction, TransactionDetail, History, HistoryDetail, Status, Category, Chat, ChatDetail
from flask_login import login_user, current_user, logout_user, login_required

title = 'VT Shop'
customerImagePath = 'Database/Pictures/User/'
itemImagePath = 'Database/Pictures/Item/'

@app.route('/')
def Home():
    # print(current_user.name)
    page = request.args.get('page', 1, type=int)
    items = Item.query.order_by(Item.sold.desc()).paginate(page=page, per_page=5)
    # page = request.args.get('page', 1, type=int)
    # items = Item.query.order_by(Item.price).paginate(page=page, per_page=2)
    return render_template('index.html', title=title+' - Index', items=items)

@app.route('/search')
def Search():
    query = request.args['search']
    page = request.args.get('page', 1, type=int)
    items = Item.query.filter(Item.name.like('%'+query+'%') | Item.description.like('%'+query+'%') | Item.id.like(query)).order_by(Item.sold.desc()).paginate(page=page, per_page=2)
    # page = request.args.get('page', 1, type=int)
    # items = Item.query.order_by(Item.price).paginate(page=page, per_page=2)
    return render_template('index.html', title=title+' - Index', items=items)

@app.route("/item/<int:item_id>", methods=['GET', 'POST'])
def ViewItem(item_id):
    item = Item.query.get_or_404(item_id)
    form = AddCartForm()
    if form.validate_on_submit():
        if form.quantity.data > item.stock:
            flash('Sorry we don\'t have that much items!', 'danger')
            return redirect(url_for('ViewItem', item_id=item_id))
        cart = Cart(quantity=form.quantity.data, user_id = current_user.id, item_id=item_id)
        db.session.add(cart)
        db.session.commit()
        flash('Item added to cart!', 'success')
        return redirect(url_for('ViewItem', item_id=item_id))
    elif request.method == 'GET':
        form.quantity.data = 1
    return render_template('item.html', title=title+' - '+item.name, item=item, form=form)

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
    cart = Cart.query.filter_by(user_id=current_user.id).all()
    total = 0
    for c in cart:
        total += c.item.price * c.quantity
    return render_template('cart.html', title=title+' - Cart', carts=cart, total=total)

def SaveItemPicture(form_picture, item_id):
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_name = str(item_id) + f_ext
    picture_path = os.path.join(app.root_path, 'static/'+itemImagePath, picture_name)
    output_size = (512, 512)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_name

@app.route('/add_item', methods=['GET', 'POST'])
@login_required
def AddItem():
    if not current_user.is_authenticated or current_user.usertype.id >= 3:
        return redirect(url_for('Home'))
    form = AddItemForm()
    categories = Category.query.all()
    allCategory = []
    for category in categories:
        allCategory.append((category.id, category.name))
    form.category_id.choices = allCategory
    if form.validate_on_submit():
        item = Item(name = form.name.data, price = form.price.data, unit=form.unit.data, description = form.description.data, category_id = form.category_id.data, stock = form.stock.data)
        if form.picture.data:
            picture_file = SaveItemPicture(form.picture.data, Item.query.order_by(Item.id.desc()).first().id+1)
            # current_user.image_file = picture_file
            item.image_file = picture_file
        db.session.add(item)
        db.session.commit()
        flash('Item Added!', 'success')
        return redirect(url_for('AddItem'))
    return render_template('addItem.html', title=title+' - Add Item', form=form)

@app.route('/edit_item', methods=['GET', 'POST'])
@login_required
def EditItem():
    if not current_user.is_authenticated or current_user.usertype.id >= 3:
        return redirect(url_for('Home'))
    categories = Category.query.all() 
    form = AddItemForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = SaveItemPicture(form.picture.data, Item.query.order_by(Item.id.desc()).first().id+1)
            current_user.image_file = picture_file
        item = Item(name = form.name.data, price = form.price.data, unit=form.unit.data, description = form.description.data, category_id = form.category_id.data, stock = form.stock.data)
        db.session.add(item)
        db.session.commit()
        flash('Item Changed!', 'success')
        return redirect(url_for('AddItem'))
    return render_template('addItem.html', title=title+' - Add Item', form=form, categories=categories)

@app.route('/add_category', methods=['GET', 'POST'])
@login_required
def AddCategory():
    if not current_user.is_authenticated or current_user.usertype.id >= 3:
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
    if not current_user.is_authenticated or current_user.usertype.id != 1:
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
    # user_image = url_for('static', filename = customerImagePath+current_user.image_file)
    # return render_template('account.html', title=title+' Account', user_image=user_image)
    return render_template('userInfo.html', title=title+' Account')

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

@app.route("/edit_user_type/<string:username>", methods=['GET', 'POST'])
@login_required
def EditUser(username):
    if not current_user.is_authenticated or current_user.usertype.id != 1:
        return redirect(url_for('Home'))
    form = ChangeUserTypeForm()
    user = User.query.filter_by(username = username).first()
    form.userType.choices = [(ut.id, ut.name) for ut in UserType.query.all()]
    if form.validate_on_submit():
        user.userType_id = form.userType.data
        db.session.commit()
        flash(username+' user type has been updated to '+user.usertype.name+"!", 'success')
        return redirect(url_for('EditUser, username=user.username'))
    elif request.method == 'GET':
        form.userType.data = user.userType_id
    return render_template('editUser.html', title=title+' - Edit User', form=form, user=user)

@app.route("/messages", methods=['GET', 'POST'])
@login_required
def UserChat():
    if current_user.usertype.id <= 2:
        return redirect(url_for('AdminChatList'))
    form = ChatForm()
    chats = ChatDetail.query.filter(ChatDetail.chat_id==current_user.id)
    if form.validate_on_submit():
        chat = Chat.query.get(current_user.id)
        if chat == None:
            chat = Chat(id=current_user.id)
            db.session.add(chat)
        else:
            chat.is_read = False
        newChat = ChatDetail(chat_id=current_user.id, user_id=current_user.id, description=form.text.data)
        db.session.add(newChat)
        db.session.commit()
        return redirect(url_for('UserChat'))
    return render_template('chatUser.html', title=title+' - Messages', form=form, chats=chats)

@app.route("/messages/<string:username>", methods=['GET', 'POST'])
@login_required
def AdminChat(username):
    if current_user.usertype.id > 2:
        return redirect(url_for('Home'))
    form = ChatForm()
    chats = ChatDetail.query.join(Chat).join(User).filter(User.username==username)
    user = User.query.filter(User.username==username).first()
    if form.validate_on_submit():
        newChat = ChatDetail(chat_id=user.id, user_id=current_user.id, description=form.text.data)
        db.session.add(newChat)
        db.session.commit()
        return redirect(url_for('AdminChat', username=username))
    return render_template('chatAdmin.html', title=title+' - Messages', form=form, chats=chats, user=user)

@app.route("/messages_list")
@login_required
def AdminChatList():
    if current_user.usertype.id > 2:
        return redirect(url_for('Home'))
    chats = Chat.query.all()
    return render_template('chatList.html', title=title+' - Messages List', chats=chats)

# @app.errorhandler(404)
# def page_not_found(e):
#     # note that we set the 404 status explicitly
#     return render_template('error.html'), 404

if __name__ == '__main__':
    app.run(debug=True)