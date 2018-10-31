import sqlite3

def ReadDB(table):

    connection = sqlite3.connect('Database/E-Commerce.db')
    cursor = connection.cursor()

    result = []
    for row in cursor.execute('SELECT * FROM '+table+' ORDER BY code'):
        result.append(row)
    
    return result

def UserCheck(email, password):
    connection = sqlite3.connect('Database/E-Commerce.db')
    cursor = connection.cursor()

    for row in cursor.execute('SELECT * FROM User'):
        if row[3] == email and row[4] == password:
            return row[0]
    
    return -1

def ReadUser(code):
    pass

# pformat = "| {:^4} | {:^4} | {:^10} | {:^10} | {:^10} |"
# pformat1 = "| {:-^4} | {:-^4} | {:-^10} | {:-^10} | {:-^10} |"
# print(pformat1.format("-","-","-","-","-"))
# print(pformat.format("ID", "Type", "Name", "Email", "Password"))
# print(pformat1.format("-","-","-","-","-"))
# for row in cursor.execute('SELECT * FROM User ORDER BY id'):
#     print(pformat.format(row[0], row[1], row[2], row[3], row[4]))
# print(pformat1.format("-","-","-","-","-"))