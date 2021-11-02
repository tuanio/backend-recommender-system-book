from app import db

class Author(db.Model):
    __tablename__ = "author"
    id = db.Column(db.Integer, primary_key = True)
    full_name = db.Column(db.String(255), nullable = True)

    