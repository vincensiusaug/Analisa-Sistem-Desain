from flask import url_for, render_template, flash, redirect
from FlaskSite import app, bcrypt
from FlaskSite.DBHandler import ReadUsernameInfo, ReadAllUser, NewUser, UserCheck
from FlaskSite.Forms import RegistrationForm, LoginForm
from FlaskSite.Models import User
from flask_login import login_user, current_user, logout_user

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
    if current_user.is_authenticated:
        return redirect(url_for('Home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashedPassword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(firstName = form.firstName.data, lastName = form.lastName.data, username = form.username.data, email = form.email.data, password = hashedPassword, address = form.address.data, phone = form.phone.data, bank = form.bank.data)
        db.session.add(user)
        db.session.commit()
        flash('Account Created', 'success')
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        NewUser(form.firstName.data, form.lastName.data, form.email.data, form.username.data, hashed_password, form.address.data, form.phone.data)
        return redirect(url_for('Login'))
    return render_template('register.html', title=title+' - Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def Login():
    if current_user.is_authenticated:
        return redirect(url_for('Home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            flash('You have been logged in!', 'success')
            return redirect(url_for('Home'))
        flash('Wrong email or password!', 'danger')

        # code = UserCheck(form.email.data, form.password.data)
        # if code:
        #     flash('You have been logged in!', 'success')
        #     return redirect(url_for('Home'))
        # else:
        #     flash('Wrong email or password!', 'danger')
    return render_template('login.html', title=title+' - Login', form=form)

@app.route('/logout')
def Logout():
    logout_user()
    flash('You have been logged out!', 'success')
    return redirect(url_for('Home'))

@app.route('/account', methods=['GET', 'POST'])
def Account():
    return render_template('account.html', title=title+' - Account')

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