# FLASK_APP=FlaskHello.py flask run
# atau
# export FLASK_APP=FlaskHello.py
# flask run
from flask import Flask, url_for, render_template
from DBReader import ReadUserNameInfo
app = Flask(__name__)

# @app.route("/")
# def hello():
#     return "Hello World! Vincent"

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('Login.html', name=name)

# @app.route('/user/<username>')
# def show_user_profile(username):
#     # show the user profile for that user
#     userInfo = ReadUserNameInfo(username)
#     returnedInfo = ("Code = %s<br>Type = %s<br>Name = %s<br>Email = %s<br>Password = %s" % (userInfo[0], userInfo[1], userInfo[2], userInfo[3], userInfo[4]))
#     return returnedInfo

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % subpath

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         return do_the_login()
#     else:
#         return show_the_login_form()

@app.route('/user/<username>')
def profile(username):
    return '{}\'s profile'.format(username)

# with app.test_request_context():
#     print(url_for('index'))
    # print(url_for('login'))
    # print(url_for('login', next='/'))
#     print(url_for('profile', username='John Doe'))

# /
# /login
# /login?next=/
# /user/John%20Doe