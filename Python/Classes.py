class User:
    def __init__(self, code, name, email, password, bankAcc, address, phone):
        self.email = email
        self.password = password
        self.name = name
        self.bankAcc = bankAcc
        self.address = address
        self.phone = phone

class Customer(User):
    def __init__(self, code, name, email, password, bankAcc, address, phone):
        super(code, name, email, password, bankAcc, address, phone)
        self.allHistory = []
        self.allTransaction = []

class Admin(User):
    def __init__(self, code, name, email, password, bankAcc, address, phone):
        super(code, name, email, password, bankAcc, address, phone)

class CategoryHandler:
    def __init__(self):
        self.category = []

class Category:
    def __init__(self, code, name, description):
        self.item = []
        self.code = code
        self.name = name
        self.description = description

class Item:
    def __init__(self):
        pass

class Cart:
    def __init__(self):
        self.cartDetail = []

class CartDetail:
    def __init__(self):
        pass

class Transaction:
    def __init__(self):
        self.transactionDetail = []

class TransactionDetail:
    def __init__(self):
        pass

class History:
    def __init__(self):
        self.historyDetail = []

class HistoryDetail:
    def __init__(self):
        pass

class TransactionStatus:
    def __init__(self):
        pass