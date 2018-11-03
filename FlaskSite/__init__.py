from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
<<<<<<< HEAD
=======
from flask_login import LoginManager
>>>>>>> 2e7d671d250c77cfd9d247f9e153b3d02bb556d7

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///static/Database/Site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
<<<<<<< HEAD
=======
loginManager = LoginManager(app)
>>>>>>> 2e7d671d250c77cfd9d247f9e153b3d02bb556d7

from FlaskSite import Routes