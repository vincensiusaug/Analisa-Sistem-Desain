import sqlite3


def Cursor():
    db = '../Database/E-Commerce.db'
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    return cursor

def ReadField(table):
    cursor = Cursor()

    result = []
    for record in cursor.execute('SELECT * FROM ' + table):
        result.append(record)
    
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

    for record in cursor.execute('SELECT * FROM user WHERE username='+str(username)):
        userRecord = {
            'code' : record[0],
            'permission' : record[1],
            'firstName' : record[2]
        }
        return record
    return -1