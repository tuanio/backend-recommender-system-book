from app import db, User

user = User(uid="blablabla", user_name="tuanio", user_email="lala@gmail.com")

db.session.add(user)
db.session.commit()
