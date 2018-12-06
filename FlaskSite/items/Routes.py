import os
from sqlalchemy import or_
from flask import url_for, render_template, flash, redirect, request, abort, Blueprint
from FlaskSite import app, bcrypt, db, mail
from FlaskSite.items.Forms import AddItemForm, EditItemForm, AddCartForm
from FlaskSite.Models import (UserType, User, Item, Category, Cart, Transaction, TransactionDetail, History, HistoryDetail,
                            Status, Category, Chat, ChatDetail, ShippingRecord, Shipping)
from flask_login import login_user, current_user, logout_user, login_required
from FlaskSite.items.Utils import SaveItemPicture

items = Blueprint('items', __name__)
title = 'VT Shop'
userImagePath = 'Database/Pictures/User/'
itemImagePath = 'Database/Pictures/Item/'
perPageItem = 5
perPageUser = 5
restrictedUser = ("Customer")
specialUser = ("Owner", "Admin")


@items.route("/item/<int:item_id>", methods=['GET', 'POST'])
def ViewItem(item_id):
    item = Item.query.get_or_404(item_id)
    form = AddCartForm()
    if form.validate_on_submit():
        if form.quantity.data > item.stock:
            flash('Sorry we don\'t have that much items!', 'danger')
            return redirect(url_for('items.ViewItem', item_id=item_id))
        cart = Cart.query.filter(Cart.customer_id == current_user.id, Cart.item_id == item.id).first()
        if cart:
            if cart.quantity + form.quantity.data > item.stock:
                flash('Sorry we don\'t have that much items!', 'danger')
                return redirect(url_for('items.ViewItem', item_id=item_id))
            else:
                cart.quantity += form.quantity.data

        else:
            cart = Cart(quantity=form.quantity.data, customer_id = current_user.id, item_id=item_id)
            db.session.add(cart)
        db.session.commit()
        flash('Item added to cart!', 'success')
        return redirect(url_for('items.ViewItem', item_id=item_id))
    elif request.method == 'GET':
        form.quantity.data = 1
    return render_template('item.html', title=title+' - '+item.name, item=item, form=form)

@items.route('/add_item', methods=['GET', 'POST'])
@login_required
def AddItem():
    if not current_user.is_authenticated or current_user.usertype.name in restrictedUser:
        return redirect(url_for('main.Home'))
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
        return redirect(url_for('items.AddItem'))
    return render_template('addItem.html', title=title+' - Add Item', form=form)

@items.route('/item/delete')
@login_required
def DeleteItem():
    item_id = request.args['item_id']
    item = Item.query.get(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Item Deleted!', 'success')
    return redirect(url_for('main.Home'))

@items.route('/item/edit', methods=['GET', 'POST'])
@login_required
def EditItem():
    if not current_user.is_authenticated or current_user.usertype.name in restrictedUser:
        return redirect(url_for('main.Home'))
    form = EditItemForm()
    item_id = request.args.get('item_id', 1, type=int)
    item = Item.query.get(item_id)
    categories = Category.query.all()
    allCategory = []
    for category in categories:
        allCategory.append((category.id, category.name))
    form.category_id.choices = allCategory
    if form.validate_on_submit():
        item.name = form.name.data
        item.price = form.price.data
        item.unit = form.unit.data
        item.description = form.description.data
        item.category_id = form.category_id.data 
        item.stock = form.stock.data
        if form.picture.data:
            picture_file = SaveItemPicture(form.picture.data, Item.query.order_by(Item.id.desc()).first().id+1)
            # current_user.image_file = picture_file
            item.image_file = picture_file
        db.session.commit()
        flash('Item Changed!', 'success')
        return redirect(url_for('items.ViewItem', item_id=item_id))
    elif request.method == 'GET':
        form.name.data = item.name
        form.price.data = item.price
        form.unit.data = item.unit
        form.description.data = item.description
        form.category_id.data = item.category_id
        form.stock.data = item.stock
    return render_template('editItem.html', title=title+' - Edit Item', form=form, categories=categories, item=item)
