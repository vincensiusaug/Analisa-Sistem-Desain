from flask import Flask, url_for, render_template
from DBReader import ReadUserNameInfo
app = Flask(__name__)
title = 'Surabaya Tech Shop'

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title=title)

@app.route('/about')
def about():
    return render_template('about.html', title=title)