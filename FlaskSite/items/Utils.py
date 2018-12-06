from FlaskSite import app
import os
from flask import url_for
from PIL import Image
from FlaskSite.Variables import *

def SaveItemPicture(form_picture, item_id):
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_name = str(item_id) + f_ext
    picture_path = os.path.join(app.root_path, 'static/'+itemImagePath, picture_name)
    output_size = (512, 512)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_name