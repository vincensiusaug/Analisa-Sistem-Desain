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
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(60), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    bank = db.Column(db.Integer, unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default = 'default.jpg')

    def __repr__(self):
        return self.firstName+" "+self.lastName
