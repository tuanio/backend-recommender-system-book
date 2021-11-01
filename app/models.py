from app import db


class Author(db.Model):
    __tablename__ = "author"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255),nullable=False)
    #relation
    book_detail = db.relationship("BookDetail",backref = "author")

    def __repr__(self):
        return "<Author({}, {})>".format(self.id, self.full_name)


class Genre(db.Model):
    __tablename__ = "genre"
    id = db.Column(db.Integer, primary_key = True)
    kind = db.Column(db.String(255),nullable=False)
    #relation
    book_genre = db.relationship("BookGenre",backref = "genre")

    def __repr__(self):
        return "<Genre ({},{})>".format(self.id, self.kind)


class BookFormat(db.Model):

    __tablename__= "bookFormat"
    id = db.Column(db.Integer,primary_key=true)
    type = db.Column(db.String(255),nullable=False)
    #relation
    bookformat_detail = db.relationship("BookFormatDetail",backref = "bookformat" )

    def __repr__(self):
        return "<BookFormat ({},{})>".format(self.id, self.type)


class BookReview(db.Model):
    __tablename__ = "bookReviews"
    id = db.Column(db.Integer,primary_key=True)
    rating = db.Column(db.Float,nullable=False)
    reviews = db.Column(db.Integer,nullable=False)
    total_ratings = db.Column(db.Integer,nullable=False)
    book_id = db.Column(db.Integer,db.ForeginKey('book.id'),nullable=False)
    # relationship one to one 
    book = db.relationship("Book",backref = backref("book",uselist=Fasle))


    def __repr__(self):
        return "<BookReview({},{},{},{},{})>".format(
            self.id,
            self.rating,
            self.reviews,
            self.total_ratings,
            self.book_id
        )


class Book(db.Model):
    __tablename__ = "book"
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(255), nullable=False)
    isbn13 = db.Column(db.String(255), nullable=False)
    title = db.Column(dv.String(255), nullable=False)
    desc = db.Column(db.String(15000))
    page = db.Column(db.Integer,nullable=False)
    image_url = db.Column(db.String(255),nullable=False)
    book_url = db.Column(db.String(255),nullable=False)
    # relation
    book_detail = db.relationship("BookDetail",backref='book')
    book_gerne = db.relationship("BookGenrne",backref='book')
    book_format_detail = db.relationship("BookFormatDetail",backref='book')

    def __repr__(self):
        return "<Book ({},{},{},{},{},{},{},{})>".format(
            self.id,
            self.isbn,
            self.isbn13,
            self.title,
            self.desc,
            self.page,
            self.image_url,
            self.book_url
        )


class BookDetail(db.Model):
    __tablename__ = "bookDetail"
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeginKey("book.id"), nullable=False)
    author_id = db.Columm(db.Integer, db.ForeginKey(
        "author.id"), nullable=False)

    def __repr__(self):
        return "<BookDetail({},{},{})>".format((self.id, self.book_id, self.author_id))


class BookGenre(db.Model):
    __tablename__ = "bookGenre"
    id = db.Column(db.Integer, primary_key=True)
    gerne_id = db.Column(db.Integer, db.ForeginKey("gerne.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeginKey("book.id"), nullable=False)

    def __repr__(self):
        return "<BookGenre({},{},{})>".format(self.id, self.gerne_id, self.book_id)


class BookFormatDetail(db.Model):
    __tablename__ = "bookFormatDetail"
    id = db.Column(db.Integer,primary_key= True)
    book_id = db.Column(db.Integer,db.ForeginKey("book.id"),nullable=False)
    book_format_id= db.Column(db.Integer , db.ForeginKey("bookformat.id"),nullable=False)

    def __repr__(self):
        return "<BookFormatDetail({},{},{})>".format(self.id, self.book_id, self.book_format_id)
