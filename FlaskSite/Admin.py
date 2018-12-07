from FlaskSite import app, db
from flask_admin import Admin, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from FlaskSite.Models import User, Item, Category, Shipping
from flask_login import current_user
from flask import url_for, redirect
from flask_admin.menu import MenuLink

class ViewPermission(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            if current_user.usertype.name == "Owner":
                return True 
        return False

class FlaskyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if current_user.is_authenticated:
            if current_user.usertype.name == "Owner":
                return super(FlaskyAdminIndexView, self).index()
        return redirect(url_for('main.Home'))



admin = Admin(app, name='VT Shop', index_view=FlaskyAdminIndexView())
# admin.add_link(MenuLink(name='Public Website'))
# admin.add_link('google.com')
admin.add_link(MenuLink(name='Back', url='/'))
admin.add_view(ViewPermission(User, db.session))
admin.add_view(ViewPermission(Item, db.session))
admin.add_view(ViewPermission(Category, db.session))
admin.add_view(ViewPermission(Shipping, db.session))