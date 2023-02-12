from HBS.models import Maxim
from HBS import db

for x in range(0,100):
    maxim = Maxim(maxim='Lorem Ipsum Dolor sit amet')
    maxim.show = True
    db.session.add(maxim)

db.session.commit()
