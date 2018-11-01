from FlaskSite import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(20), unique=False, nullable=False)
    lastName = db.Column(db.String(20), unique=False, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(60), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    bank = db.Column(db.Integer, unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

    def __repr__(self):
        return "User('{self.firstName}', '{self.lastName}', '{self.image_file}')"