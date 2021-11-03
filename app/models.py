from app import db

# db.relationship(name_of_class, back_ref ="name_of_relation", lazy= True)


class Author(db.Model):
    __tablename__ = "author"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    # relation one to many
    book_detail = db.relationship("BookDetail", backref="author", lazy=True)

    def __repr__(self):
        return "<Author({}, {})>".format(self.id, self.full_name)


class Genre(db.Model):
    __tablename__ = "genre"
    id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.String(255))
    # relation one to many
    book_genre = db.relationship("BookGenre", backref="genre")

    def __repr__(self):
        return "<Genre ({},{})>".format(self.id, self.kind)


class BookFormat(db.Model):

    __tablename__ = "bookformat"
    id = db.Column(db.Integer, primary_key=True)
    type_ = db.Column(db.String(255))
    # relation one to many
    bookformat_detail = db.relationship(
        "BookFormatDetail", backref="bookformat", lazy=True)

    def __repr__(self):
        return "<BookFormat ({},{})>".format(self.id, self.type)


class Book(db.Model):
    __tablename__ = "book"
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(255))
    isbn13 = db.Column(db.String(255))
    title = db.Column(db.String(255))
    desc = db.Column(db.String(15000))
    pages = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255))
    book_url = db.Column(db.String(255), nullable=False)
    # relation one to many
    book_detail = db.relationship(
        "BookDetail", backref="book_detail", lazy=True)
    book_genre = db.relationship("BookGenre", backref="book_genre", lazy=True)
    book_format_detail = db.relationship(
        "BookFormatDetail", backref="book_format", lazy=True)
    book_review = db.relationship(
        "BookReview", back_populates="book", uselist=False)

    def __repr__(self):
        return "<Book ({},{},{},{},{},{},{},{})>".format(
            self.id,
            self.isbn,
            self.isbn13,
            self.title,
            self.desc,
            self.pages,
            self.image_url,
            self.book_url
        )


class BookReview(db.Model):
    __tablename__ = 'bookreview'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float, nullable=False)
    reviews = db.Column(db.Integer, nullable=False)
    total_ratings = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"))
    # relationship one to one (khong duoc )
    book = db.relationship("Book", back_populates="book_review")

    def __repr__(self):
        return "<BookReview({},{},{},{},{})>".format(
            self.id,
            self.rating,
            self.reviews,
            self.total_ratings,
            self.book_id
        )


class BookDetail(db.Model):
    __tablename__ = "bookdetail"
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey(
        "author.id"), nullable=False)

    def __repr__(self):
        return "<BookDetail({},{},{})>".format((self.id, self.book_id, self.author_id))


class BookGenre(db.Model):
    __tablename__ = "bookgenre"
    id = db.Column(db.Integer, primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)

    def __repr__(self):
        return "<BookGenre({},{},{})>".format(self.id, self.genre_id, self.book_id)


class BookFormatDetail(db.Model):
    __tablename__ = "bookformatdetail"
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    book_format_id = db.Column(
        db.Integer, db.ForeignKey("bookformat.id"), nullable=False)

    def __repr__(self):
        return "<BookFormatDetail({},{},{})>".format(self.id, self.book_id, self.book_format_id)
