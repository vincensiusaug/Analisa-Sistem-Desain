from datetime import datetime
from FlaskSite import db, loginManager
from flask_login import UserMixin

@loginManager.user_loader
def LoadUser(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    permission = db.Column(db.Integer, default = 1)
    firstName = db.Column(db.String(20), unique=False, nullable=False)
    lastName = db.Column(db.String(20), unique=False, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(60), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    bank = db.Column(db.Integer, unique=False, nullable=True)
    image_file = db.Column(db.String(20), nullable=False, default = 'user-default.jpg')
    cart = db.relationship('Cart', backref='user', lazy=True)
    transaction = db.relationship('Transaction', backref='user', lazy=True)
    history = db.relationship('History', backref='user', lazy=True)

    def __repr__(self):
        return self.firstName+" "+self.lastName

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    description = db.Column(db.String(200), unique=False, nullable=True)
    items = db.relationship('Item', backref='categories', lazy=True)

    def __repr__(self):
        return self.name

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    price = db.Column(db.Integer, unique=False, nullable=False)
    unit = db.Column(db.String(20), unique=False, nullable=True)
    description = db.Column(db.String(200), unique=False, nullable=True)
    stock = db.Column(db.Integer, unique=False, nullable=False)
    sold = db.Column(db.Integer, default=0)
    image_file = db.Column(db.String(20), nullable=False, default = 'item-default.jpg')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    # cart = db.relationship('CartDetail', backref='item', lazy=True)
    # transaction = db.relationship('Transaction', backref='itemTransaction', lazy=True)
    # history = db.relationship('History', backref='itemHistory', lazy=True)


    def __repr__(self):
        return self.name

class CartDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, unique=False, nullable=False)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)

    def __repr__(self):
        return self.id

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cartDetail = db.relationship('CartDetail', backref='cart', lazy=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return self.id

class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), unique=False, nullable=True)
    transaction = db.relationship('Transaction', backref='status', lazy=True)
    history = db.relationship('History', backref='status', lazy=True)

    def __repr__(self):
        return self.id

class TransactionDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, unique=False, nullable=False)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)

    def __repr__(self):
        return self.id

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    transactionDetail = db.relationship('TransactionDetail', backref='transaction', lazy=True)

    def __repr__(self):
        return self.id

class HistoryDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, unique=False, nullable=False)
    history_id = db.Column(db.Integer, db.ForeignKey('history.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)

    def __repr__(self):
        return self.id

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    historyDetail = db.relationship('HistoryDetail', backref='history', lazy=True)

    def __repr__(self):
        return self.id


db.create_all()
