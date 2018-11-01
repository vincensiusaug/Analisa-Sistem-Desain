import sqlite3

db = 'PythonFlask/static/Database/E-Commerce.db'

def ReadField(table):
    result = []
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        for record in cursor.execute('SELECT * FROM ' + table):
            result.append(record)
    
    return result

def ReadAllUser():
    result = []
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()

        for record in cursor.execute('SELECT * FROM user'):
            result.append({
                'code' : record[0],
                'permission' : record[1],
                'firstName' : record[2],
                'lastName' : record[3],
                'email' : record[4],
                'username' : record[5],
                'password' : record[6],
                'address' : record[7],
                'phone' : record[8]
            })
    
    return result

def UserCheck(email, password):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()

        for code in cursor.execute("SELECT code FROM user WHERE email LIKE'"+email+"' AND password LIKE '"+password+"'"):
            return code
        # if code[0]:
        #     print(code[0])
        #     print(email)
        #     print(password)
        #     return code
    
    return False

def ReadUserCodeInfo(code):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()

        for record in cursor.execute('SELECT * FROM user WHERE code='+str(code)):
            return record
    return -1

def ReadUsernameInfo(username):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()

        for record in cursor.execute("SELECT * FROM user WHERE username LIKE '"+username+"'"):
            userRecord = {
                'code' : record[0],
                'permission' : record[1],
                'firstName' : record[2],
                'lastName' : record[3],
                'email' : record[4],
                'username' : record[5],
                'password' : record[6],
                'address' : record[7],
                'phone' : record[8]
            }
            return userRecord
    return {
            'code' : "",
            'permission' : "",
            'firstName' : "",
            'lastName' : "",
            'email' : "",
            'username' : "",
            'password' : "",
            'address' : "",
            'phone' : ""
        }

def NewUser(fn, ln, em, un, pw, ad, ph):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        values = (fn, ln, em, un, pw, ad, ph)
        sql = "INSERT INTO user (firstName, lastName, email, username, password, address, phone) VALUES (?,?,?,?,?,?,?)"

        cursor.execute(sql, values)
        connection.commit()