import os
from sqlalchemy import or_
from PIL import Image
from flask import url_for, render_template, flash, redirect, request, abort, Blueprint
from FlaskSite import app, bcrypt, db, mail
from FlaskSite.transactions.Forms import TransactionForm
from FlaskSite.Models import (UserType, User, Item, Category, Cart, Transaction, TransactionDetail, History, HistoryDetail,
                            Status, Category, Chat, ChatDetail, ShippingRecord, Shipping)
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

transactions = Blueprint('transactions', __name__)
title = 'VT Shop'
userImagePath = 'Database/Pictures/User/'
itemImagePath = 'Database/Pictures/Item/'
perPageItem = 5
perPageUser = 5
restrictedUser = ("Customer")
specialUser = ("Owner", "Admin")

@transactions.route('/transaction', methods=['GET', 'POST'])
@login_required
def AllTransaction():
    status_id = request.form.get('statusSelect', 0, type=int)
    allStatus = []
    allStatus.append((0, "All transaction"))
    for status in Status.query.all():
        allStatus.append((status.id, status.description))
    if current_user.usertype.name in restrictedUser:
        transactions = Transaction.query.filter(Transaction.customer_id == current_user.id).all()
    else:
        if status_id != 0:
            transactions = Transaction.query.join(Status).filter(Status.id==status_id).all()
        else:
            transactions = Transaction.query.all()
    return render_template('transactionList.html', title=title+' - Transaction', transactions=transactions, allStatus=allStatus, selected=status_id)
    # else:
    #     return render_template('transactionAdmin.html', title=title+' - Transaction')

@transactions.route('/transaction/<int:transaction_id>/remove')
@login_required
def DeleteTransaction(transaction_id):
    # transaction_id = request.args['transaction_id']
    transaction = Transaction.query.get(transaction_id)
    for detail in TransactionDetail.query.filter(TransactionDetail.transaction_id == transaction_id):
        Item.query.get(detail.item_id).stock += detail.quantity
        db.session.delete(detail)
    db.session.delete(transaction)
    db.session.commit()
    return redirect(url_for('transactions.AllTransaction'))

@transactions.route('/transaction/<int:transaction_id>/view')
@login_required
def ViewTransaction(transaction_id):
    transaction = Transaction.query.get(transaction_id)
    details = TransactionDetail.query.filter(TransactionDetail.transaction_id == transaction_id).all()
    ships = []
    for ship in Shipping.query.all():
        ships.append((ship.id, ship.name))
    return render_template('transactionDetailSpecial.html', title=title+' - Transaction', details=details, transaction=transaction, ships=ships)
    # return render_template('transactionDetailSpecial.html', title=title+' - Transaction', details=details, transaction=transaction)

@transactions.route('/transaction/<int:transaction_id>/confirm')
@login_required
def ConfirmPaymentTransaction(transaction_id):
    Transaction.query.get(transaction_id).status_id = 2
    db.session.commit()
    return redirect(url_for('transactions.ViewTransaction', transaction_id=transaction_id))

@transactions.route('/transaction/<int:transaction_id>/courrier')
@login_required
def CourrierTransaction(transaction_id):
    print("shipping_number")
    shipping_id = request.args['courrier']
    shipping_number = request.args['shipping_number']
    transaction = Transaction.query.get(transaction_id)
    transaction.status_id = 3
    shipping_record = ShippingRecord(shipping_id=shipping_id, shipping_number=shipping_number, transaction_id=transaction_id)
    db.session.add(shipping_record)
    transaction.shipping_record.append(shipping_record)
    db.session.commit()
    return redirect(url_for('transactions.ViewTransaction', transaction_id=transaction_id))

@transactions.route('/transaction/<int:transaction_id>/recieve')
@login_required
def RecievedTransaction(transaction_id):
    transaction = Transaction.query.get(transaction_id)
    details = TransactionDetail.query.filter(TransactionDetail.transaction_id == transaction_id).all()
    shipping_record = ShippingRecord.query.filter(transaction_id==transaction.id).first()
    history = History(status_id = 4, customer_id=transaction.customer_id)
    db.session.add(history)
    db.session.commit()
    shipping_record.transaction_id = None
    shipping_record.history_id = history.id
    history.shipping_record.append(shipping_record)
    for detail in details:
        hd = HistoryDetail(quantity=detail.quantity, history_id=history.id, item_id=detail.item_id)
        db.session.add(hd)
        history.total_price += detail.item.price * detail.quantity
        history.historyDetail.append(hd)
        db.session.delete(detail)
    db.session.delete(transaction)
    db.session.commit()
    return redirect(url_for('histories.ViewHistory', history_id=history.id))

@transactions.route('/transaction/<int:transaction_id>/bad')
@login_required
def BadTransaction(transaction_id):
    transaction = Transaction.query.get(transaction_id)
    details = TransactionDetail.query.filter(TransactionDetail.transaction_id == transaction_id).all()
    shipping_record = ShippingRecord.query.filter(transaction_id==transaction.id).first()
    history = History(status_id = 5, customer_id=transaction.customer_id)
    db.session.add(history)
    db.session.commit()
    shipping_record.transaction_id = None
    shipping_record.history_id = history.id
    history.shipping_record.append(shipping_record)
    for detail in details:
        hd = HistoryDetail(quantity=detail.quantity, history_id=history.id, item_id=detail.item_id)
        db.session.add(hd)
        history.total_price += detail.item.price * detail.quantity
        history.historyDetail.append(hd)
        db.session.delete(detail)
    db.session.delete(transaction)
    db.session.commit()
    return redirect(url_for('histories.ViewHistory', history_id=history.id))