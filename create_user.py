from HBS.models import User
from HBS import db

user = User(username='admin', email='admin@gmail.com')
user.set_password('admin')
db.session.add(user)
db.session.commit()
print('Done!')