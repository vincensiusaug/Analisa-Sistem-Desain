import os
from sqlalchemy import or_
from PIL import Image
from flask import url_for, render_template, flash, redirect, request, abort, Blueprint
from FlaskSite import db
from FlaskSite.Models import (UserType, User, Item, Category, Cart, Transaction, TransactionDetail, History, HistoryDetail,
                            Status, Category, Chat, ChatDetail, ShippingRecord, Shipping)
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from FlaskSite.Variables import *

histories = Blueprint('histories', __name__)

@histories.route('/history')
@login_required
def AllHistory():
    status_id = request.form.get('statusSelect', 0, type=int)
    allStatus = []
    allStatus.append((0, "All transaction"))
    for status in Status.query.all():
        allStatus.append((status.id, status.description))
    if current_user.usertype.name in restrictedUser:
        histories = History.query.filter(History.customer_id == current_user.id).all()
    else:
        if status_id != 0:
            histories = History.query.join(Status).filter(Status.id==status_id).all()
        else:
            histories = History.query.all()
    return render_template('historyList.html', title=title+' - History', histories=histories, allStatus=allStatus, selected=status_id)

@histories.route('/history/<int:history_id>/view')
@login_required
def ViewHistory(history_id):
    history = History.query.get(history_id)
    details = HistoryDetail.query.filter(HistoryDetail.history_id == history_id).all()
    return render_template('historyDetail.html', title=title+' - Transaction', details=details, history=history)
