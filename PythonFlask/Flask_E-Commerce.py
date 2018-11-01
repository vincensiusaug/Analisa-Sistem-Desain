from flask import Flask, url_for, render_template
from DBReader import ReadUserNameInfo
app = Flask(__name__)
title = 'VT Shop'

@app.route('/')
@app.route('/home')
def Home():
    return render_template('home.html', title=title+' - Home')

@app.route('/about')
def About():
    return render_template('about.html', title=title+' - About')

@app.route('/login')
def Login():
    return render_template('login.html', title=title+' - Login')

if __name__ == '__main__':
    app.run(debug=True)