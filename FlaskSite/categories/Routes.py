import os
from sqlalchemy import or_
from PIL import Image
from flask import url_for, render_template, flash, redirect, request, abort, Blueprint
from FlaskSite import app, bcrypt, db, mail
from FlaskSite.categories.Forms import AddCategoryForm, EditCategoryForm
from FlaskSite.Models import (UserType, User, Item, Category, Cart, Transaction, TransactionDetail, History, HistoryDetail,
                            Status, Category, Chat, ChatDetail, ShippingRecord, Shipping)
from flask_login import login_user, current_user, logout_user, login_required

categories = Blueprint('categories', __name__)
title = 'VT Shop'
userImagePath = 'Database/Pictures/User/'
itemImagePath = 'Database/Pictures/Item/'
perPageItem = 5
perPageUser = 5
restrictedUser = ("Customer")
specialUser = ("Owner", "Admin")


@categories.route('/add_category', methods=['GET', 'POST'])
@login_required
def AddCategory():
    if not current_user.is_authenticated or current_user.usertype.name in restrictedUser:
        return redirect(url_for('main.Home'))
    form = AddCategoryForm()
    if form.validate_on_submit():
        category = Category(name = form.name.data, description = form.description.data)
        db.session.add(category)
        db.session.commit()
        flash('Category Added!', 'success')
        return redirect(url_for('categories.AddCategory'))
    return render_template('addCategory.html', title=title+' - Add Category', form=form)

@categories.route('/category/edit', methods=['GET', 'POST'])
@login_required
def EditCategory():
    if not current_user.is_authenticated or current_user.usertype.name in restrictedUser:
        return redirect(url_for('main.Home'))
    form = EditCategoryForm()
    category_id = request.args.get('category_id', 1, type=int)
    category = Category.query.get(category_id)
    if form.validate_on_submit():
        category.name = form.name.data
        category.description = form.description.data
        db.session.commit()
        flash('Category Changed!', 'success')
        return redirect(url_for('categories.ViewCategory', category_id=category_id))
    elif request.method == 'GET':
        form.name.data = category.name
        form.description.data = category.description
    return render_template('editCategory.html', title=title+' - Edit Category', form=form, category=category)

@categories.route("/category/<int:category_id>")
def ViewCategory(category_id):
    category = Category.query.get(category_id)
    items = Item.query.filter_by(category_id=category_id).all()
    return render_template('viewCategory.html', title=title+' - '+category.name, category=category, items=items)

