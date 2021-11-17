from app import app, db, status_code
from app.models import *
from app.utils import make_response, make_data
from pprint import pprint
import operator
from sqlalchemy.sql import case


@app.route('/', methods=['GET'])
def index():
    return make_response(dict(msg="Hello world"))


@app.route('/api/get-book/<int:book_id>')
def get_book(book_id: int):
    '''
    return information of a book
    # thiếu genre
    '''
    book = Book.query.filter_by(id=book_id).first().get_data()

    author_ids = list(map(lambda x: x.author_id,
                      BookDetail.query.filter_by(book_id=book_id).all()))
    authors_names = list(map(lambda x: x.get_data(),
                         Author.query.filter(Author.id.in_(author_ids)).all()))

    book_review = BookReview.query.filter_by(
        book_id=book_id).first().get_data()

    ret_data = book
    ret_data.update(book_review)
    ret_data['authors'] = authors_names

    return make_response(make_data(data=ret_data, msg="Return a book successfully!"))


@app.route('/api/update-count-author-genre/<int:user_id>/<int:book_id>')
def update_count_author_genre(user_id: int, book_id: int):
    '''
    update count for author and genre of a book
    '''
    author_ids = list(map(lambda x: x[0], BookDetail.query.filter_by(
        book_id=book_id).with_entities(BookDetail.author_id).all()))

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
            user_id=user_id, author_id=auth_id), author_ids))
        db.session.bulk_save_objects(list_author_count)

    # update data genre count
    genre_ids = list(map(lambda x: x[0], BookGenre.query.filter_by(
        book_id=book_id).with_entities(BookGenre.genre_id).all()))
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
            user_id=user_id, genre_id=genre_id), genre_ids))
        db.session.bulk_save_objects(list_genre_count)

    db.session.commit()

    return make_response(make_data(msg="Update author and genre count successfully!"))


@app.route('/api/get-book-similar/<int:book_id>')
def get_book_similar(book_id: int):
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


@app.route('/api/get-top-100-books')
def get_top_100_books():
    LIMIT_BOOKS = 100
    list_book_id = BookReview.query.order_by(
        BookReview.weighted_rating.desc()
    ).with_entities(
        BookReview.book_id
    ).limit(LIMIT_BOOKS).all()
    list_book_id = map(lambda x: x[0], list_book_id)
    list_book = list(map(lambda x: x.get_data(),
                     Book.query.filter(Book.id.in_(list_book_id)).all()))
    return make_response(make_data(data=dict(list_book=list_book), msg="Return top 100 books"))


@app.route('/api/update-user-rating/<int:user_id>/<int:book_id>/<int:user_rating>')
def update_user_rating(user_id: int, book_id: int, user_rating: int):
    book_rating = BookRating(
        rating=user_rating, user_id=user_id, book_id=book_id)
    db.session.add(book_rating)
    db.session.commit()
    return make_response(make_data(msg="Update rating successfully!"))


@app.route('/api/get-list-book-rated/<int:user_id>')
def get_list_book_rated(user_id: int):
    book_rating = BookRating.query.filter_by(user_id=user_id).with_entities(BookRating.book_id, BookRating.rating).all()
    book_rated = list(map(lambda x: Book.query.filter(Book.id == x[0]).first().get_data(), book_rating))
    for i, _ in enumerate(book_rated):
        book_rated[i]['user_rating'] = book_rating[i][1]
    return make_response(make_data(data=dict(list_books=book_rated), msg="Return list book rated successfully!"))


@app.route('/api/update-favorite/<int:user_id>/<int:book_id>')
def update_favorite(user_id: int, book_id: int):
    try:
        msg = "Update book favorite successfully!"
        # when we already have
        book_favorite = BookFavorite.query.filter_by(
            user_id=user_id, book_id=book_id).first()
        assert book_favorite  # check is not none
        book_favorite.is_favorite ^= True
    except:
        msg = "Create book favorite successfully!"
        book_favorite = BookFavorite(user_id=user_id, book_id=book_id)
        db.session.add(book_favorite)
    db.session.commit()
    return make_response(make_data(msg=msg))


@app.route('/api/get-book-favorited/<int:user_id>')
def get_book_favorited(user_id: int):
    favorited_book_ids = list(map(lambda x: x[0], BookFavorite.query.filter_by(
        user_id=user_id, is_favorite=True).with_entities(BookFavorite.book_id).all()))
    favorited_books = list(map(lambda x: x.get_data(
    ), Book.query.filter(Book.id.in_(favorited_book_ids)).all()))[::-1]
    return make_response(make_data(data=dict(list_books=favorited_books), msg="Return favorited book sucessfully!"))


# @app.route('/system/')