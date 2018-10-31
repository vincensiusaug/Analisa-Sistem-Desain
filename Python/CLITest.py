from DBReader import ReadDB, UserCheck

def UserAuth(email, password):
    AuthResult = UserCheck(email, password)
    if AuthResult == -1:
        print("Wrong Email or password")
    else:
        print(AuthResult)

def ShowAllUser():
    allUser = ReadDB("user")
    pformat = "| {:^4} | {:^4} | {:^10} | {:^10} | {:^10} |"
    pformat1 = "| {:-^4} | {:-^4} | {:-^10} | {:-^10} | {:-^10} |"
    print(pformat1.format("-","-","-","-","-"))
    print(pformat.format("Code", "Type", "Name", "Email", "Password"))
    print(pformat1.format("-","-","-","-","-"))
    # for row in allUser:
    #     print(row)
    for row in allUser:
        print(pformat.format(row[0], row[1], row[2], row[3], row[4]))
    print(pformat1.format("-","-","-","-","-"))

ShowAllUser()

email = input("Masukan email = ")
password = input("Masukan password = ")
print("Checking...")
UserAuth(email, password)