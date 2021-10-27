from app import db

 
class Author(db.Model):
    __tablename__="author"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255),nullable=False)
    def __init__(self, full_name):
        self.full_name=full_name
    def __repr__(self):
        return "<Author ({},{})>".format(
            self.id,
            self.full_name
        )


