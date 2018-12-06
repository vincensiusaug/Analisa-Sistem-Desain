from flask import url_for, render_template, flash, redirect, request, abort, Blueprint
from FlaskSite import app, bcrypt, db, mail
from FlaskSite.admins.Forms import ChangeUserTypeForm
from FlaskSite.Models import (UserType, User, Item, Category, Cart, Transaction, TransactionDetail, History, HistoryDetail,
                            Status, Category, Chat, ChatDetail, ShippingRecord, Shipping)
from flask_login import login_user, current_user, logout_user, login_required
from FlaskSite.Variables import *

admins = Blueprint('admins', __name__)

@admins.route('/view_users')
@login_required
def ViewUser():
    if not current_user.is_authenticated or current_user.usertype.name != "Owner":
        abort(403)
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.userType_id).paginate(page=page, per_page=perPageUser)
    
    return render_template('viewUser.html', title=title+' - View User', users=users)

@admins.route('/search_user')
def SearchUser():
    if not current_user.is_authenticated or current_user.usertype.name != "Owner":
        abort(403)
    query = request.args['search']
    page = request.args.get('page', 1, type=int)
    users = User.query.filter(User.username.like('%'+query+'%') | User.firstName.like('%'+query+'%') | User.lastName.like(query)).order_by(User.userType_id).paginate(page=page, per_page=perPageUser)
    # page = request.args.get('page', 1, type=int)
    # items = Item.query.order_by(Item.price).paginate(page=page, per_page=2)
    return render_template('viewUser.html', title=title+' - Search User', users=users)

@admins.route("/edit_user_type/<string:username>", methods=['GET', 'POST'])
@login_required
def EditUser(username):
    if not current_user.is_authenticated or current_user.usertype.name != "Owner":
        abort(403)
    form = ChangeUserTypeForm()
    user = User.query.filter_by(username = username).first()
    form.userType.choices = [(ut.id, ut.name) for ut in UserType.query.all()]
    if form.validate_on_submit():
        user.userType_id = form.userType.data
        db.session.commit()
        flash(username+' user type has been updated to '+user.usertype.name+"!", 'success')
        return redirect(url_for('admins.EditUser', username=user.username))
    elif request.method == 'GET':
        form.userType.data = user.userType_id
    return render_template('editUser.html', title=title+' - Edit User', form=form, user=user)