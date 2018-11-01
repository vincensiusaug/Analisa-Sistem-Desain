import sqlite3


def Cursor():
    db = 'PythonFlask/static/Database/E-Commerce.db'
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    return cursor

def ReadField(table):
    cursor = Cursor()

    result = []
    for record in cursor.execute('SELECT * FROM ' + table):
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
    cursor = Cursor()

    for record in cursor.execute('SELECT * FROM User'):
        if record[3] == email and record[4] == password:
            return record[0]
    
    return -1

def ReadUserCodeInfo(code):
    cursor = Cursor()

    for record in cursor.execute('SELECT * FROM user WHERE code='+str(code)):
        return record
    return -1

def ReadUsernameInfo(username):
    cursor = Cursor()

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