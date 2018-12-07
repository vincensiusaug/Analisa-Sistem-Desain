from FlaskSite import app, db
from flask_admin import Admin, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from FlaskSite.Models import User, Item, Category, Shipping, UserType, Cart, Status, Transaction, ShippingRecord, History, Chat, ChatDetail, HistoryDetail, TransactionDetail
from flask_login import current_user
from flask import url_for, redirect
from flask_admin.menu import MenuLink

class ViewPermission(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            if current_user.usertype.name == "Owner":
                return True 
        return False

class OwnerIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if current_user.is_authenticated:
            if current_user.usertype.name == "Owner":
                return super(OwnerIndexView, self).index()
        return redirect(url_for('main.Home'))



admin = Admin(app, name='VT Shop', index_view=OwnerIndexView(url='/vtshop_owner'))
# admin.add_sub_category(name="Links", parent_name="Team")
admin.add_link(MenuLink(name='Back', url='/'))

admin.add_view(ViewPermission(User, db.session, category='User', name='User List'))
admin.add_view(ViewPermission(UserType, db.session, category='User', name='User Permission'))

admin.add_view(ViewPermission(Item, db.session, category='Item', name='Item List'))

admin.add_view(ViewPermission(Category, db.session, category='Category'))

admin.add_view(ViewPermission(Transaction, db.session, category='Transaction'))
admin.add_view(ViewPermission(TransactionDetail, db.session, category='Transaction'))
admin.add_view(ViewPermission(Status, db.session, category='Transaction'))

admin.add_view(ViewPermission(Shipping, db.session, category='Shipping'))
admin.add_view(ViewPermission(ShippingRecord, db.session, category='Shipping'))

admin.add_view(ViewPermission(History, db.session, category='History'))
admin.add_view(ViewPermission(HistoryDetail, db.session, category='History'))

admin.add_view(ViewPermission(Chat, db.session, category='Chat'))
admin.add_view(ViewPermission(ChatDetail, db.session, category='Chat'))