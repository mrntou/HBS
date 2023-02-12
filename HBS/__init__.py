from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from .admin_views import MyAdminIndexView
import json



app = Flask(__name__)
app.config.from_file('config.json',load=json.load)


db = SQLAlchemy(app)
login_manager = LoginManager(app)
admin = Admin(app, template_mode="bootstrap4", index_view=MyAdminIndexView())




from HBS import routes
