from flask import url_for, render_template, flash, redirect
from FlaskSite import app, bcrypt
from FlaskSite.DBHandler import ReadUsernameInfo, ReadAllUser, NewUser, UserCheck
from FlaskSite.Forms import RegistrationForm, LoginForm
from FlaskSite.Models import User


title = 'VT Shop'

@app.route('/')
@app.route('/home')
def Home():
    return render_template('home.html', title=title+' - Home')

@app.route('/about')
def About():
    return render_template('about.html', title=title+' - About')

@app.route('/register', methods=['GET', 'POST'])
def Register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account Created', 'success')
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        NewUser(form.firstName.data, form.lastName.data, form.email.data, form.username.data, hashed_password, form.address.data, form.phone.data)
        return redirect(url_for('Login'))
    return render_template('register.html', title=title+' - Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def Login():
    form = LoginForm()
    if form.validate_on_submit():
        code = UserCheck(form.email.data, form.password.data)
        if code:
            flash('You have been logged in!', 'success')
            return redirect(url_for('Home'))
        else:
            flash('Wrong email or password!', 'danger')
    return render_template('login.html', title=title+' - Login', form=form)

@app.route('/allUser')
@app.route('/allUser/')
@app.route('/user')
@app.route('/user/')
def AllUser():
    return render_template('allUserInfo.html', title=title+' - All User', allUser=ReadAllUser())

@app.route('/user/<username>')
def UserInfo(username=None):
    ReadUsernameInfo(username)
    return render_template('userInfo.html',title=title+' - '+username, info=ReadUsernameInfo(username))

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('error.html'), 404

if __name__ == '__main__':
    app.run(debug=True)