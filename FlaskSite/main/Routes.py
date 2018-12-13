import os
from sqlalchemy import or_
from PIL import Image
from flask import url_for, render_template, flash, redirect, request, abort, Blueprint
from FlaskSite import app, bcrypt, db, mail
from FlaskSite.main.Forms import *
from FlaskSite.Models import (UserType, User, Item, Category, Cart, Transaction, TransactionDetail, History, HistoryDetail,
                            Status, Category, Chat, ChatDetail, ShippingRecord, Shipping)
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

main = Blueprint('main', __name__)
title = 'VT Shop'
userImagePath = 'Database/Pictures/User/'
itemImagePath = 'Database/Pictures/Item/'
perPageItem = 5
perPageUser = 5
restrictedUser = ("Customer")
specialUser = ("Owner", "Admin")

@main.route('/')
def Home():
    # print(current_user.name)
    page = request.args.get('page', 1, type=int)
    items = Item.query.order_by(Item.sold.desc()).paginate(page=page, per_page=perPageItem)
    return render_template('index.html', title=title+' - Index', items=items)

@main.route('/search')
def Search():
    query = request.args['search']
    page = request.args.get('page', 1, type=int)
    items = Item.query.filter(Item.name.like('%'+query+'%') | Item.description.like('%'+query+'%') | Item.id.like(query)).order_by(Item.sold.desc()).paginate(page=page, per_page=perPageItem)
    # page = request.args.get('page', 1, type=int)
    # items = Item.query.order_by(Item.price).paginate(page=page, per_page=2)
    return render_template('index.html', title=title+' - Search', items=items)

@main.route('/about')
def About():
    return render_template('about.html', title=title+' - About')

@main.route("/test")
def TestPage():
    return render_template('test.html', title=title+' - AI')