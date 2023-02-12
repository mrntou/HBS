from flask_admin import AdminIndexView, BaseView, expose
from flask_login import current_user
from flask import abort


class MyAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        return self.render("admin/index.html")

    def is_accessible(self):
        if not current_user.is_authenticated:
            abort(404)
        if current_user.is_admin == True:
            return True
        else:
            abort(404)