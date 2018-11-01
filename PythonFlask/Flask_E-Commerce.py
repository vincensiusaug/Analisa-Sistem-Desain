from flask import Flask, url_for, render_template
from DBReader import ReadUserNameInfo
app = Flask(__name__)
title = 'Surabaya Tech Shop'

@app.route('/')
def index():
    return render_template('index.html', title=title)