# from DBReader import ReadField, UserCheck, ReadUserCode
import sqlite3
from flask_bcrypt import Bcrypt
import getpass

bcrypt = Bcrypt()
db = 'FlaskSite/static/Database/E-Commerce.db'

def UserAuth(email, password):
    AuthResult = UserCheck(email, password)
    if AuthResult == -1:
        print("\nThe Email or Password you entered is incorrect")
    else:
        print("\nLogged in\nCode = "+str(AuthResult))
        print()
        userInfo = ReadUserCode(AuthResult)
        pformat = "| {:^5} | {:^4} | {:^20} | {:^20} | {:^10} |"
        pformat1 = "| {:-^5} | {:-^4} | {:-^20} | {:-^20} | {:-^10} |"
        print(pformat1.format("-","-","-","-","-"))
        print(pformat.format("Code", "Type", "Name", "Email", "Password"))
        print(pformat1.format("-","-","-","-","-"))
        print(pformat.format(userInfo[0], userInfo[1], userInfo[2], userInfo[3], userInfo[4]))
        print(pformat1.format("-","-","-","-","-"))

def ShowAllUser():
    allUser = ReadField("user")

    pformat = "| {:^5} | {:^4} | {:^20} | {:^20} | {:^10} |"
    pformat1 = "| {:-^5} | {:-^4} | {:-^20} | {:-^20} | {:-^10} |"
    print(pformat1.format("-","-","-","-","-"))
    print(pformat.format("Code", "Type", "Name", "Email", "Password"))
    print(pformat1.format("-","-","-","-","-"))

    for record in allUser:
        print(pformat.format(record[0], record[1], record[2], record[3], record[4]))
    print(pformat1.format("-","-","-","-","-"))
    print()

def UserCheck(email, password):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        for code in cursor.execute("SELECT code FROM user WHERE email LIKE '"+email+"'"):
            code = str(code[0])
            print(code)
            for userPassword in cursor.execute("SELECT password FROM user WHERE code LIKE '"+code+"'"):
                # hashedPassword = userPassword
                # print (hashedPassword)
                print(userPassword)
                passwordCheck = bcrypt.check_password_hash(userPassword[0], password)
                if passwordCheck == True:
                    return code    
    return False

print(UserCheck('wkwkwk@vtg.com', 'feriawan125'))

# ShowAllUser()
# print("Login")
# email = input("Email = ")
# password = getpass.getpass("Password = ")
# print("Checking...")
# UserAuth(email, password)
