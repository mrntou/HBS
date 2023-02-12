from HBS import app,db, login_manager, admin
from flask_login import current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_admin.contrib.sqla import ModelView
from datetime import datetime



@login_manager.user_loader
def load_user(user):
    return User.query.get(int(user))



# Kullanici veritabani
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    email = db.Column(db.String(80), nullable=False)
    is_admin = db.Column(db.Boolean(), default=False)
    maxims = db.relationship('Maxim', backref='maxims', lazy=True)
    daily_limit = db.Column(db.Integer, default=10)
    tasks_today = db.Column(db.Integer, default=0)
    last_task_date = db.Column(db.DateTime, default=datetime.utcnow)

    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def __repr__(self):
        return self.username



# Ozlu sozler veritabani
class Maxim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    maxim = db.Column(db.Text)
    category = db.Column(db.String())
    author = db.Column(db.String(80))
    timestamp = db.Column(db.DateTime(), default=datetime.now)
    active = db.Column(db.Boolean())
    show = db.Column(db.Boolean(), default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))






class AdminModelView(ModelView):
    pass



admin.add_view(AdminModelView(Maxim, db.session))
admin.add_view(AdminModelView(User, db.session))
