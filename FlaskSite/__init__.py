from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from FlaskSite.Config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.jinja_env.auto_reload = True
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
loginManager = LoginManager(app)
loginManager.login_view = 'users.Login'
loginManager.login_message_category = 'info'

mail = Mail(app)

from FlaskSite.admins.Routes import admins
from FlaskSite.carts.Routes import carts
from FlaskSite.categories.Routes import categories
from FlaskSite.chats.Routes import chats
from FlaskSite.histories.Routes import histories
from FlaskSite.items.Routes import items
from FlaskSite.main.Routes import main
from FlaskSite.transactions.Routes import transactions
from FlaskSite.users.Routes import users

app.register_blueprint(admins)
app.register_blueprint(carts)
app.register_blueprint(categories)
app.register_blueprint(chats)
app.register_blueprint(histories)
app.register_blueprint(items)
app.register_blueprint(main)
app.register_blueprint(transactions)
app.register_blueprint(users)
