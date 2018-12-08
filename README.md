# Analisa Sistem Desain (E-Commerce)
  

username = superuser
password = superuser

Required package (install using pip3)
pillow
sqlalchemy
flask
flask-login
flask-mail
flask-sqlalchemy
flask-bcrypt
flask-admin

Menentukan environment variable
export SECRET_KEY='5791628bb0b13ce0c676dfde280ba245'
export SQLALCHEMY_DATABASE_URI='sqlite:///static/Database/Site.db'
export MAIL_USERNAME="email" - Pengaturan safe app email harus dimatikan
export MAIL_PASSWORD="password"



Cara menjalankan:
1. Set working directory pada folder ini
2. $ ./FlaskRun
3. Buka 0.0.0.0:5000/