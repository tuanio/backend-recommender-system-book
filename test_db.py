from app import db ,Author,Genre,BookFormat,BookReview,Book,BookDetail,BookGenre,BookFormatDetail

author =  Author(
    full_name = "hmtoan"
)

db.session.add(author)
db.session.commit()

genre = Genre(
    kind = "honor"
)

db.session.add(genre)
db.session.commit()

book_format = BookFormat(
    type_ = "bia cung "
)

db.session.add(book_format)
db.session.commit()

newbook = Book(
    isbn = "abc",
    isbn13 = "255",
    title = "sach hay ",
    desc = "first demo",
    pages = 150,
    image_url ="goodbooks.com/sachhay.png",
    book_url = "goodbooks.com/sachhay"
)
db.session.add(newbook)
db.session.commit()

book_review = BookReview(
    rating = 3.5,
    reviews = 250,
    total_ratings = 150,
    book_id = newbook.id
)

db.session.add(book_review)
db.session.commit()

book_detail = BookDetail(
    book_id = newbook.id,
    author_id = author.id
)

db.session.add(book_detail)
db.session.commit()

book_genre = BookGenre(
    genre_id = genre.id,
    book_id = newbook.id
)

db.session.add(book_genre)
db.session.commit()

book_format_detail = BookFormatDetail(
    book_id = newbook.id,
    book_format_id = book_format.id
)
db.session.add(book_format_detail)
db.session.commit()
