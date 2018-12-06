import os
from sqlalchemy import or_
from PIL import Image
from flask import url_for, render_template, flash, redirect, request, abort, Blueprint
from FlaskSite import app, bcrypt, db, mail
from FlaskSite.chats.Forms import ChatForm
from FlaskSite.Models import (UserType, User, Item, Category, Cart, Transaction, TransactionDetail, History, HistoryDetail,
                            Status, Category, Chat, ChatDetail, ShippingRecord, Shipping)
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from FlaskSite.Variables import *

chats = Blueprint('chats', __name__)

@chats.route("/messages", methods=['GET', 'POST'])
@login_required
def UserChat():
    if current_user.usertype.id <= 2:
        return redirect(url_for('chats.ChatList'))
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
        return redirect(url_for('chats.UserChat'))
    return render_template('chatUser.html', title=title+' - Messages', form=form, chats=chats)

@chats.route("/messages/<string:username>", methods=['GET', 'POST'])
@login_required
def AdminChat(username):
    if current_user.usertype.id > 2:
        return redirect(url_for('main.Home'))
    form = ChatForm()
    chats = ChatDetail.query.join(Chat).join(User).filter(User.username==username)
    user = User.query.filter(User.username==username).first()
    chat = Chat.query.get(user.id)
    chat.is_read = True
    db.session.commit()
    if form.validate_on_submit():
        newChat = ChatDetail(chat_id=user.id, user_id=current_user.id, description=form.text.data)
        db.session.add(newChat)
        db.session.commit()
        return redirect(url_for('chats.AdminChat', username=username))
    return render_template('chatAdmin.html', title=title+' - Messages', form=form, chats=chats, user=user)

@chats.route("/messages_list")
@login_required
def ChatList():
    if current_user.usertype.id > 2:
        return redirect(url_for('main.Home'))
    page = request.args.get('page', 1, type=int)
    chats = Chat.query.join(User).filter(User.userType_id==3).order_by(Chat.is_read).paginate(page=page, per_page=perPageUser)
    return render_template('chatList.html', title=title+' - Messages List', chats=chats)

@chats.route('/search_chat')
def SearchChat():
    if current_user.usertype.id > 2:
        return redirect(url_for('main.Home'))
    query = request.args['search']
    page = request.args.get('page', 1, type=int)
    chats = Chat.query.join(User).filter(User.username.like('%'+query+'%')).order_by(Chat.is_read).paginate(page=page, per_page=perPageUser)
    return render_template('chatList.html', title=title+' - Search User', chats=chats)