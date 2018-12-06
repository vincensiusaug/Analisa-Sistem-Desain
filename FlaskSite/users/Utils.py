from flask_mail import Message
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image
from FlaskSite import app, bcrypt, db, mail
import os
from flask import url_for
from FlaskSite.Variables import *

def SaveUserPicture(form_picture):
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_name = current_user.username + f_ext
    picture_path = os.path.join(app.root_path, 'static/'+userImagePath, picture_name)
    output_size = (125, 125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)
    return picture_name

def SendResetEmail(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@vtshop.com',
                  recipients=[user.email])
    msg.body = '''To reset your password, visit the following link:
{:}
If you did not make this request then simply ignore this email and no changes will be made.
'''.format(url_for('users.ResetToken', token=token, _external=True))
    mail.send(msg)