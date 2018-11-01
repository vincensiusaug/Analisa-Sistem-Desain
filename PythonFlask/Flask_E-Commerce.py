from flask import Flask, url_for, render_template
from DBReader import ReadUsernameInfo, ReadAllUser
from Forms import RegistrationForm, LoginForm
app = Flask(__name__)
app.config['SECRET_KEY'] = '12h9817ywd198whd918hw10921027109wjd109284vu12fn10'
title = 'VT Shop'

@app.route('/')
@app.route('/home')
def Home():
    return render_template('home.html', title=title+' - Home')

@app.route('/about')
def About():
    return render_template('about.html', title=title+' - About')

# @app.route('/login')
# def Login():
#     return render_template('Login.html', title=title+' - Login')

@app.route('/register', methods=['GET', 'POST'])
def Register():
    form = RegistrationForm()
    return render_template('register.html', title=title+' - Register', form=form)

@app.route('/login')
def Login():
    form = LoginForm()
    return render_template('login.html', title=title+' - Login', form=form)

@app.route('/allUser')
@app.route('/allUser/')
@app.route('/user')
@app.route('/user/')
def AllUser():
    return render_template('allUserInfo.html', title=title+' - All User', allUser=ReadAllUser())

@app.route('/user/<username>')
def User(username=None):
    ReadUsernameInfo(username)
    return render_template('userInfo.html',title=title+' - '+username, info=ReadUsernameInfo(username))

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('error.html'), 404

if __name__ == '__main__':
    app.run(debug=True)