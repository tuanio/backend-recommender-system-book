from app import app, db, status_code
from app.models import *
from app.utils import make_response
from pprint import pprint
import operator
from sqlalchemy.sql import case


@app.route('/', methods=['GET'])
def index():
    return make_response(dict(msg="Hello world"))


@app.route('/api/get-book/<int:user_id>/<int:book_id>')
def get_book(user_id: int, book_id: int):
    '''
    get data of a book:
    '''
    book = Book.query.filter_by(id=book_id).first().get_data()

    author_ids = list(map(lambda x: x.author_id,
                      BookDetail.query.filter_by(book_id=book['id']).all()))
    authors_names = list(map(lambda x: x.get_data(),
                         Author.query.filter(Author.id.in_(author_ids)).all()))

    book_review = BookReview.query.filter_by(
        book_id=book['id']).first().get_data()

    ret_data = book
    ret_data.update(book_review)
    ret_data['authors'] = authors_names

    # update data author count
    try:
        # when author already have
        author_count = AuthorCount.query.filter(
            AuthorCount.user_id == user_id,
            AuthorCount.author_id.in_(author_ids)
        ).all()
        assert author_count
        for auth in author_count:
            auth.numbers_counts += 1
    except:
        # when not row queried
        list_author_count = list(map(lambda auth_id: AuthorCount(
            user_id=user_id, author_id=auth_id, numbers_counts=1), author_ids))
        db.session.bulk_save_objects(list_author_count)

    # update data genre count
    book_genres = BookGenre.query.filter_by(book_id=book['id']).all()
    genre_ids = list(map(lambda x: x.genre_id, book_genres))
    try: 
        # when author already have
        genre_count = GenreCount.query.filter(
            GenreCount.user_id == user_id,
            GenreCount.genre_id.in_(genre_ids)
        ).all()
        assert genre_count
        for genre in genre_count:
            genre.numbers_counts += 1
    except:
        # when not row queried
        list_genre_count = list(map(lambda genre_id: GenreCount(
            user_id=user_id, genre_id=genre_id, numbers_counts=1), genre_ids))
        db.session.bulk_save_objects(list_genre_count)
    
    db.session.commit()

    return make_response(dict(
        data=ret_data,
        msg="Return book data successfully!",
        status_code=status_code['SUCCESS']
    ))


@app.route('/api/book-similar/<int:book_id>')
def book_similar(book_id: int):
    similar_books = BookDescriptionSimilarities.query.filter_by(
        book_id=book_id).all()
    similar_books = list(map(lambda x: x.book_recommend_id, similar_books))
    similar_books = list(map(lambda x: Book.query.filter_by(
        id=x).first().get_data(), similar_books))
    return make_response(dict(
        data=similar_books,
        msg="Return top 10 book successfully!",
        status_code=status_code['SUCCESS']
    ))
