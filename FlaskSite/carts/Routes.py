import os
from sqlalchemy import or_
from PIL import Image
from flask import url_for, render_template, flash, redirect, request, abort, Blueprint
from FlaskSite import db
from FlaskSite.Models import (UserType, User, Item, Category, Cart, Transaction, TransactionDetail, History, HistoryDetail,
                            Status, Category, Chat, ChatDetail, ShippingRecord, Shipping)
from flask_login import login_user, current_user, logout_user, login_required
from FlaskSite.Variables import *

carts = Blueprint('carts', __name__)

@carts.route('/cart')
@login_required
def UserCart():
    cart = Cart.query.filter_by(customer_id=current_user.id).all()
    total = 0
    for c in cart:
        total += c.item.price * c.quantity
    
    return render_template('cart.html', title=title+' - Cart', carts=cart, total=total)

@carts.route('/cart/remove')
@login_required
def DeleteCart():
    cart_id = request.args['cart_id']
    cart = Cart.query.get(cart_id)
    db.session.delete(cart)
    db.session.commit()
    return redirect(url_for('carts.UserCart'))

@carts.route('/cart/buy')
@login_required
def BuyCart():
    carts = Cart.query.filter_by(customer_id=current_user.id).all()
    transaction = Transaction(status_id = 1, customer_id=current_user.id)
    db.session.add(transaction)
    db.session.commit()
    for cart in carts:
        Item.query.get(cart.item_id).stock -= cart.quantity
        detail = TransactionDetail(quantity = cart.quantity, transaction_id = transaction.id, item_id = cart.item_id)
        db.session.add(detail)
        transaction.total_price = transaction.total_price + (cart.item.price * cart.quantity)
        db.session.delete(cart)
    db.session.commit()
    return redirect(url_for('transactions.AllTransaction'))