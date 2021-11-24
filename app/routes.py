from app import app, db, status_code
from app.models import *
from app.utils import make_response, make_data
from flask import request
from flask_cors import cross_origin
from pprint import pprint
import operator
from sqlalchemy.sql import case


@app.route('/', methods=['GET'])
@cross_origin()
def index():
    return make_response(dict(msg="Hello world"))


@app.route('/api/get-book/<int:book_id>', methods=['GET'])
@cross_origin()
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


@app.route('/api/update-count-author-genre/<int:user_id>/<int:book_id>', methods=['PUT'])
@cross_origin()
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


@app.route('/api/get-book-similar/<int:book_id>', methods=['GET'])
@cross_origin()
def get_book_similar(book_id: int):
    similar_books = BookDescriptionSimilarities.query.filter_by(
        book_id=book_id).all()
    similar_books = list(map(lambda x: x.book_recommend_id, similar_books))
    similar_books = list(map(lambda x: Book.query.filter_by(
        id=x).first().get_data(cols=['id', 'image_url']), similar_books))

    return make_response(dict(
        data=dict(list_books=similar_books),
        msg="Return top 10 book successfully!",
        status_code=status_code['SUCCESS']
    ))


@app.route('/api/get-top-100-books', methods=['GET'])
@cross_origin()
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


@app.route('/api/update-user-rating/<int:user_id>/<int:book_id>/<int:user_rating>', methods=['PUT'])
@cross_origin()
def update_user_rating(user_id: int, book_id: int, user_rating: int):
    try:
        book_rating = BookRating.query.filter_by(
            user_id=user_id, book_id=book_id).first()
        assert book_rating  # check where is None
        # nếu vượt qua cái assert thì nghĩa là có rồi, chỉ update lại thôi
        if user_rating == 0:  # Lượt call mặc định
            return make_response(make_data(msg="There's no change on this user rating"))
        book_rating.rating = user_rating  # còn không thì cập nhật lại
    except:
        book_rating = BookRating(
            rating=user_rating, user_id=user_id, book_id=book_id)
        db.session.add(book_rating)

    db.session.commit()
    return make_response(make_data(msg="Update rating successfully!"))


@app.route('/api/get-list-book-rated/<int:user_id>', methods=['GET'])
@cross_origin()
def get_list_book_rated(user_id: int):
    try:
        book_rating = BookRating.query.filter_by(user_id=user_id).filter_by(
            rating > 0).with_entities(BookRating.book_id, BookRating.rating).all()
        book_rated = list(map(lambda x: Book.query.filter(
            Book.id == x[0]).first().get_data(), book_rating))
        for i, _ in enumerate(book_rated):
            book_rated[i]['user_rating'] = book_rating[i][1]
    except Exception as e:
        return make_response(make_data(data=dict(error=str(e)), msg="Return list book rated fail!", status='FAILURE'))
    return make_response(make_data(data=dict(list_books=book_rated), msg="Return list book rated successfully!"))


@app.route('/api/update-favorite/<int:user_id>/<int:book_id>', methods=['PUT'])
@cross_origin()
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


@app.route('/api/get-book-favorited/<int:user_id>', methods=['GET'])
@cross_origin()
def get_book_favorited(user_id: int):
    favorited_book_ids = list(map(lambda x: x[0], BookFavorite.query.filter_by(
        user_id=user_id, is_favorite=True).with_entities(BookFavorite.book_id).all()))
    favorited_books = list(map(lambda x: x.get_data(cols=['id', 'image_url']), Book.query.filter(Book.id.in_(favorited_book_ids)).all()))[::-1]
    return make_response(make_data(data=dict(list_books=favorited_books), msg="Return favorited book sucessfully!"))


@app.route('/api/test/create-mock-user', methods=['POST'])
@cross_origin()
def create_mock_user():

    try:
        data = request.get_json(force=True)
        db.session.add(User(**data))
        db.session.commit()
    except Exception as e:
        return make_response(make_data(dict(error=str(e)), msg="Create user fail!", status='FAILURE'))

    return make_response(make_data(msg="Create user successfully!"))


@app.route('/api/get-all-user', methods=['GET'])
@cross_origin()
def get_all_user():

    try:
        list_users = list(map(lambda x: x.get_data(), User.query.all()))
    except Exception as e:
        return make_response(make_data(dict(error=str(e)), msg="Return list user fail", status='FAILURE'))

    return make_response(make_data(dict(list_users=list_users), msg="Return list user successfully!"))


@app.route('/api/get-reading-list-history/<int:user_id>', methods=['GET'])
@cross_origin()
def get_reading_list_history(user_id):

    try:
        book_rating = BookRating.query.filter_by(
            user_id=user_id).with_entities(BookRating.book_id).all()
        book_rating_ids = list(map(lambda x: x[0], book_rating))

        list_book = list(map(lambda x: x.get_data(cols=['id', 'image_url']), Book.query.filter(
            Book.id.in_(book_rating_ids)).all()))
            
    except Exception as e:
        return make_response(make_data(dict(error=str(e)), msg="Return reading list history fail", status='FAILURE'))

    return make_response(make_data(dict(list_book=list_book), msg="Return reading list history successfully!"))


@app.route('/api/get-all-authors', methods=['GET'])
@cross_origin()
def get_all_authors():
    try:
        list_authors = list(map(lambda x: x.get_data(), Author.query.all()))
    except Exception as e:
        return make_response(make_data(dict(error=str(e)), msg="Return list authors fail!", status='FAILURE'))

    return make_response(make_data(dict(list_authors=list_authors), msg="Return list authors successfully!"))


@app.route('/api/get-all-genres', methods=['GET'])
@cross_origin()
def get_all_genres():
    try:
        list_genres = list(map(lambda x: x.get_data(), Genre.query.all()))
    except Exception as e:
        return make_response(make_data(dict(error=str(e)), msg="Return list genres fail!", status='FAILURE'))

    return make_response(make_data(dict(list_genres=list_genres), msg="Return list genres successfully!"))
    

@app.route('/api/get-list-books-by-author-genre/<int:author_id>/<int:genre_id>', methods=['GET'])
@cross_origin()
def get_list_books_by_author_genre(author_id: int, genre_id: int):
    try:

        list_book_id_1 = BookDetail.query.filter_by(author_id=author_id).with_entities(BookDetail.book_id).all()
        list_book_id_1 = map(lambda x: x[0], list_book_id_1)

        list_book_id_2 = BookGenre.query.filter_by(genre_id=genre_id).with_entities(BookGenre.book_id).all()
        list_book_id_2 = map(lambda x: x[0], list_book_id_2)

        list_match_book_ids = set(list_book_id_1) | set(list_book_id_2)

        list_books = Book.query.filter(Book.id.in_(list_match_book_ids)).all()
        list_books = list(map(lambda x: x.get_data(), list_books))
        
    except Exception as e:
        return make_response(make_data(dict(error=str(e)), msg="Return list genres fail!", status='FAILURE'))

    return make_response(make_data(dict(nums_books=len(list_books), list_books=list_books), msg="Return list genres successfully!"))


# @app.route('/system/')
