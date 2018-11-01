from flask import Flask, url_for, render_template
from DBReader import ReadUsernameInfo, ReadField
app = Flask(__name__)
title = 'VT Shop'

dummyData = [
    {
        'name' : 'Vincensius Augustino',
        'permission' : '1',
        'email' : 'vin',
        'username' : 'vincensius',
        'password' : 'vin'
    },
    {
        'name' : 'Feriawan',
        'permission' : '1',
        'email' : 'fer',
        'username' : 'feriawan',
        'password' : 'fer'
    }
    ]

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

@app.route('/register')
def Register():
    return render_template('login.html', title=title+' - Register')

@app.route('/allUser')
@app.route('/allUser/')
@app.route('/user')
@app.route('/user/')
def AllUser():
    return render_template('allUserInfo.html', title=title+' - All User', allUser=ReadField("user"))

@app.route('/user/<username>')
def User(username=None):
    ReadUsernameInfo(username)
    return render_template('userInfo.html',title=title+' - ', info=ReadUsernameInfo(username))

if __name__ == '__main__':
    app.run(debug=True)