from FlaskSite import app
import os
from flask import url_for
from PIL import Image
from FlaskSite.Variables import *

def SaveItemPicture(form_picture):
    random_hex = os.urandom(16).hex()
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/'+itemImagePath, picture_name)
    output_size = (itemOutputSize)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_name