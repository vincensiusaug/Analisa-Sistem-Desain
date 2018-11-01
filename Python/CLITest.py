from DBReader import ReadField, UserCheck, ReadUser

def UserAuth(email, password):
    AuthResult = UserCheck(email, password)
    if AuthResult == -1:
        print("\nThe Email or Password you entered is incorrect")
    else:
        print("\nLogged in\nCode = "+str(AuthResult))
        print()
        userInfo = ReadUser(AuthResult)
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

ShowAllUser()
print("Login")
email = input("Email = ")
password = input("Password = ")
print("Checking...")
UserAuth(email, password)
