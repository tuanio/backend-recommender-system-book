from enum import unique
from app import db
from app.utils import get_subset

# db.relationship(name_of_class, back_ref ="name_of_relation", lazy= True)
db.drop_all()
db.metadata.clear()


class Author(db.Model):
    __tablename__ = "author"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    # relation one to many
    book_detail = db.relationship("BookDetail", backref="author", lazy=True)
    # author_counts = db.relationship("AuthorCount", backref="author_counts", lazy=True)

    def get_data(self):
        just_get = ['id', 'full_name']
        return get_subset(self.__dict__, just_get)

    def __repr__(self):
        return "<Author({}, {})>".format(self.id, self.full_name)


class Genre(db.Model):
    __tablename__ = "genre"
    id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.String(255))
    # relation one to many
    book_genre = db.relationship("BookGenre", backref="genre")
    # genre_counts = db.relationship("GenreCount", backref="genre_counts", lazy=True)

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
    pages = db.Column(db.Integer)
    image_url = db.Column(db.String(255))
    book_url = db.Column(db.String(255))
    # relation one to many
    book_detail = db.relationship(
        "BookDetail", backref="book_detail", lazy=True)
    book_genre = db.relationship("BookGenre", backref="book_genre", lazy=True)
    book_format_detail = db.relationship(
        "BookFormatDetail", backref="book_format", lazy=True)
    book_review = db.relationship(
        "BookReview", back_populates="book", uselist=False)
    book_description = db.relationship(
        "BookDescriptionSimilarities", backref="book_description", lazy=True)
    # book_rating = db.relationship("BookRating",backref="book_rating", lazy=True)

    def get_data(self):
        just_get = ['id', 'isbn', 'isbn13', 'title',
                    'desc', 'pages', 'image_url', 'book_url']
        return get_subset(self.__dict__, just_get)

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
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), unique=True)
    weighted_rating = db.Column(db.Float)
    # relationship one to one (khong duoc )
    book = db.relationship("Book", back_populates="book_review")

    def get_data(self):
        just_get = ['id', 'rating', 'reviews', 'total_ratings']
        return get_subset(self.__dict__, just_get)

    def __repr__(self):
        return "<BookReview({},{},{},{},{},{})>".format(
            self.id,
            self.rating,
            self.reviews,
            self.total_ratings,
            self.book_id,
            self.weighted_rating
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


class BookDescriptionSimilarities(db.Model):
    __tablename__ = "bookdescriptionsimilarities"
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    book_recommend_id = db.Column(db.Integer)

    def __repr__(self):
        return "<BookDescription({},{},{})>".format(self.id, self.book_id, self.book_recommend_id)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    uid = db.Column(db.String(255), nullable=False, unique=True)
    user_name = db.Column(db.String(255), nullable=False)
    user_email = db.Column(db.String(255))
    # relation one to many with keyword
    keywords = db.relationship("KeyWord", backref="keywords", lazy=True)
    user_rating = db.relationship(
        "BookRating", backref="user_rating", lazy=True)
    author_counts = db.relationship(
        "AuthorCount", backref="author_counts", lazy=True)
    genre_counts = db.relationship("GenreCount", backref="genre_counts")

    def __repr__(self):
        return "<User({},{},{},{})>".format(self.id, self.uid, self.user_name, self.user_email)


class KeyWord(db.Model):
    __tablename__ = "keyword"
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return "<KeyWord({},{},{})>".format(self.id, self.keyword, self.user_id)


class BookRating(db.Model):
    __tablename__ = "bookrating"
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return "<BookRating({},{},{},{})>".format(self.id, self.rating, self.book_id, self.user_id)


class AuthorCount(db.Model):
    __tablename__ = "authorcount"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    numbers_counts = db.Column(db.Integer, nullable=False, default=0)
    author_id = db.Column(db.Integer, db.ForeignKey(
        "author.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return "<AuthorCount ({},{},{},{})>".format(self.id, self.numbers_counts, self.author_id, self.user_id)


class GenreCount(db.Model):
    __tablename__ = "genrecount"
    id = db.Column(db.Integer, primary_key=True)
    numbers_counts = db.Column(db.Integer, nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return "<GenreCount ({},{},{},{})>".format(self.id, self.numbers_counts, self.genre_id, self.user_id)
