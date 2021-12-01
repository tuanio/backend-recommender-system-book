import time
import numpy as np
from pprint import pprint
import concurrent.futures as cf
from collections import Counter

from flask import request
from flask_cors import cross_origin

from app.models import *
from app import app, db
from app.utils import make_response, make_data

from sqlalchemy.orm import load_only
from sqlalchemy import and_

from sklearn.linear_model import Ridge
from sklearn.tree import DecisionTreeRegressor


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
    try:
        book = Book.query.filter_by(id=book_id).first().get_data()

        author_ids = list(map(lambda x: x.author_id,
                              BookDetail.query.filter_by(book_id=book_id).all()))
        
        authors_names = Author.query.filter(Author.id.in_(author_ids)).all()
        authors_names = list(map(lambda x: x.get_data(['full_name'])['full_name'], authors_names))

        book_review = BookReview.query.filter_by(
            book_id=book_id).first().get_data()

        book_genre_id = BookGenre.query.filter_by(
            book_id=book['id']).with_entities(BookGenre.genre_id).all()
        book_genre_id = list(map(lambda x: x[0], book_genre_id))

        genres = Genre.query.filter(Genre.id.in_(book_genre_id)).all()
        genres = list(map(lambda x: x.get_data(['kind'])['kind'], genres))

        ret_data = book
        ret_data.update(book_review)
        ret_data['authors'] = authors_names
        ret_data['genres'] = genres
    except Exception as e:
        return make_response(make_data(dict(error=str(e)), msg="Return a book fail!", status='FAILURE'))

    return make_response(make_data(data=ret_data, msg="Return a book successfully!"))

@app.route('/api/get-all-authors', methods=['GET'])
@cross_origin()
def get_all_authors():
    try:
        list_authors = list(map(lambda x: x.get_data(), Author.query.all()))
    except Exception as e:
        return make_response(make_data(dict(error=str(e)), msg="Return list authors fail!", status='FAILURE'))

    return make_response(make_data(dict(list_authors=list_authors), msg="Return list authors successfully!"))


@app.route('/api/get-all-users', methods=['GET'])
@cross_origin()
def get_all_user():

    try:
        list_users = list(map(lambda x: x.get_data(), User.query.all()))
    except Exception as e:
        return make_response(make_data(dict(error=str(e)), msg="Return list user fail", status='FAILURE'))

    return make_response(make_data(dict(list_users=list_users), msg="Return list user successfully!"))


@app.route('/api/get-all-genres', methods=['GET'])
@cross_origin()
def get_all_genres():
    try:
        list_genres = list(map(lambda x: x.get_data(), Genre.query.all()))
    except Exception as e:
        return make_response(make_data(dict(error=str(e)), msg="Return list genres fail!", status='FAILURE'))

    return make_response(make_data(dict(list_genres=list_genres), msg="Return list genres successfully!"))


@app.route('/api/update-count-author-genre/<int:user_id>/<int:book_id>', methods=['PUT'])
@cross_origin()
def update_count_author_genre(user_id: int, book_id: int):
    '''
    update count for author and genre of a book
    '''
    try:
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
    except Exception as e:
        return make_response(make_data(dict(error=str(e)), msg="Update author and genre count fail!", status='FAILURE'))

    return make_response(make_data(msg="Update author and genre count successfully!"))


@app.route('/api/get-book-similar/<int:book_id>', methods=['GET'])
@cross_origin()
def get_book_similar(book_id: int):
    try:
        similar_books = BookDescriptionSimilarities.query.filter_by(
            book_id=book_id).all()
        similar_books = list(map(lambda x: x.book_recommend_id, similar_books))
        
        weighted_rating = BookReview.query.filter(BookReview.book_id.in_(similar_books)).with_entities(BookReview.weighted_rating).all()
        
        similar_books = list(map(lambda x: Book.query.filter_by(id=x).first().get_data(cols=['id', 'image_url', 'title']), similar_books))
        similar_books = [dict(item, rating=rating[0]) for item, rating in zip(similar_books, weighted_rating)]
        
    except Exception as e:
        return make_response(make_data(dict(error=str(e)), msg="Return top 10 book similar fail!", status='FAILURE'))

    return make_response(make_data(dict(list_books=similar_books), msg="Return top 10 book similar successfully!"))


@app.route('/api/get-top-100-books', methods=['GET'])
@cross_origin()
def get_top_100_books():
    LIMIT_BOOKS = 100

    try:
        list_book_data = BookReview.query.order_by(
            BookReview.weighted_rating.desc()
        ).with_entities(
            BookReview.book_id,
            BookReview.weighted_rating
        ).limit(LIMIT_BOOKS).all()
        list_book_id = map(lambda x: x[0], list_book_data)
        list_book = list(map(lambda x: x.get_data(
            cols=['id', 'image_url', 'title']), Book.query.filter(Book.id.in_(list_book_id)).all()))

        list_book = [dict(item, rating=rating[1]) for item, rating in zip(list_book, list_book_data)]

    except Exception as e:
        return make_response(make_data(dict(error=str(e)), msg="Return top 100 books fail!", status='FAILURE'))

    return make_response(make_data(data=dict(list_book=list_book), msg="Return top 100 books successfully!"))


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
        book_rating = BookRating.query.filter_by(user_id=user_id).filter(
            BookRating.rating > 0).with_entities(BookRating.book_id, BookRating.rating).all()
        list_book = list(map(lambda x: Book.query.filter(
            Book.id == x[0]).first().get_data(['id', 'image_url', 'title']), book_rating))
        list_book = [dict(item, rating=rating[1]) for item, rating in zip(list_book, book_rating)]
    except Exception as e:
        return make_response(make_data(data=dict(error=str(e)), msg="Return list book rated fail!", status='FAILURE'))
    return make_response(make_data(data=dict(list_books=list_book), msg="Return list book rated successfully!"))


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
    try:
        favorited_book_ids = list(map(lambda x: x[0], BookFavorite.query.filter_by(
            user_id=user_id, is_favorite=True).with_entities(BookFavorite.book_id).all()))
        

        favorited_books = list(map(lambda x: x.get_data(
            cols=['id', 'image_url', 'title']), Book.query.filter(Book.id.in_(favorited_book_ids)).all()))[::-1]
        
    except Exception as e:
        return make_response(make_data(dict(error=str(e)), msg="Return favorited book fail!", status='FAILURE'))

    return make_response(make_data(data=dict(list_books=favorited_books), msg="Return favorited book sucessfully!"))


@app.route('/api/create-user', methods=['POST'])
@cross_origin()
def create_user():

    try:
        data = request.get_json(force=True)
        user = User(**data)
        db.session.add(user)
        db.session.commit()

        book_review = BookReview.query.options(
            load_only(*['book_id', 'weighted_rating'])).all()

        def create_object(data):
            return RecommendInformation(
                user_id=user.id,
                book_id=data.book_id,
                author_weight=data.weighted_rating,
                genre_weight=data.weighted_rating
            )

        with cf.ThreadPoolExecutor() as exe:
            list_objects = list(exe.map(create_object, book_review))

        db.session.bulk_save_objects(list_objects)
        db.session.commit()

    except Exception as e:
        return make_response(make_data(dict(error=str(e)), msg="Create user fail!", status='FAILURE'))

    return make_response(make_data(dict(user_id=user.id), msg="Create user successfully!"))

@app.route('/api/get-user/<int:user_id>')
@cross_origin()
def get_user(user_id: int):

    try:
        user = User.query.filter_by(id=user_id).first().get_data()
    except:
        return make_response(make_data(dict(error=str(e)), msg="Return user info fail!", status='FAILURE'))

    return make_response(make_data(dict(user=user), msg="Create user successfully!"))


@app.route('/api/get-reading-list-history/<int:user_id>', methods=['GET'])
@cross_origin()
def get_reading_list_history(user_id):

    try:
        book_rating = BookRating.query.filter_by(
            user_id=user_id).with_entities(BookRating.book_id, BookRating.rating).all()
        book_rating_ids = list(map(lambda x: x[0], book_rating))

        list_book = list(map(lambda x: x.get_data(cols=['id', 'image_url', 'title']), Book.query.filter(
            Book.id.in_(book_rating_ids)).all()))
        list_book = [dict(item, rating=rating[1]) for item, rating in zip(list_book, book_rating)]


    except Exception as e:
        return make_response(make_data(dict(error=str(e)), msg="Return reading list history fail", status='FAILURE'))

    return make_response(make_data(dict(list_book=list_book), msg="Return reading list history successfully!"))


@app.route('/api/get-list-books-by-author-genre/<int:author_id>/<int:genre_id>', methods=['GET'])
@cross_origin()
def get_list_books_by_author_genre(author_id: int, genre_id: int):
    LIMIT_BOOK = 30

    try:

        list_book_id_1 = BookDetail.query.filter_by(
            author_id=author_id).with_entities(BookDetail.book_id).all()
        list_book_id_1 = map(lambda x: x[0], list_book_id_1)

        list_book_id_2 = BookGenre.query.filter_by(
            genre_id=genre_id).with_entities(BookGenre.book_id).all()
        list_book_id_2 = map(lambda x: x[0], list_book_id_2)

        list_match_book_ids = set(list_book_id_1) | set(list_book_id_2)

        weighted_rating = BookReview.query.filter(BookReview.book_id.in_(list_match_book_ids)).with_entities(BookReview.weighted_rating).all()

        list_books = Book.query.filter(Book.id.in_(list_match_book_ids)).limit(LIMIT_BOOK).all()
        list_books = list(map(lambda x: x.get_data(cols=['id', 'image_url', 'title']), list_books))
        
        list_books = [dict(item, rating=rating[0]) for item, rating in zip(list_books, weighted_rating)]

    except Exception as e:
        return make_response(make_data(dict(error=str(e)), msg="Return list genres fail!", status='FAILURE'))

    return make_response(make_data(dict(no_books=len(list_books), list_books=list_books), msg="Return list genres successfully!"))


@app.route('/api/get-list-book-recommend-by-author/<int:user_id>', methods=['GET'])
@cross_origin()
def get_list_book_recommend_by_author(user_id: int):
    LIMIT_BOOK = 30

    try:
        X = np.load('data/author_features.npy')
        recommend_info_origin = RecommendInformation.query.filter_by(
            user_id=user_id).all()

        list_book_id = list(map(lambda x: x.book_id, recommend_info_origin))

        user_rating_list = BookRating.query.filter(
            and_(BookRating.user_id == user_id, BookRating.rating > 0)).all()

        update_rating = {
            user.book_id: user.rating for user in user_rating_list}

        recommend_info = list(map(lambda x: x.get_data(
            ['book_id', 'author_weight']), recommend_info_origin))

        for idx, info in enumerate(recommend_info):
            rated = update_rating.get(info['book_id'], None)
            if rated:
                info['author_weight'] = rated

        y = list(map(lambda x: x['author_weight'], recommend_info))

        model = Ridge(alpha=1e-5, random_state=12)
        model.fit(X, y)

        y_pred = model.predict(X).tolist()

        for idx in range(len(recommend_info_origin)):
            recommend_info_origin[idx].author_weight = y_pred[idx]
        db.session.commit()

        list_book_final = [book_id for weight, book_id in sorted(zip(y_pred, list_book_id), reverse=True, key=lambda x: x[0])][:LIMIT_BOOK]
        weighted_rating = BookReview.query.filter(BookReview.book_id.in_(list_book_final)).with_entities(BookReview.weighted_rating).all()

        list_book = Book.query.filter(Book.id.in_(list_book_final)).all()
        list_book = list(map(lambda x: x.get_data(['id', 'image_url', 'title']), list_book))

        list_book = [dict(item, rating=rating[0]) for item, rating in zip(list_book, weighted_rating)]

        
    except Exception as e:
        return make_response(make_data(dict(error=str(e)), msg="Return list recommend books by author fail!", status='FAILURE'))

    return make_response(make_data(dict(list_book=list_book), msg="Return list recommend books by author successfully!"))


@app.route('/api/get-list-book-recommend-by-genre/<int:user_id>', methods=['GET'])
@cross_origin()
def get_list_book_recommend_by_genre(user_id: int):
    LIMIT_BOOK = 30

    try:
        X = np.load('data/genre_features.npy')
        recommend_info_origin = RecommendInformation.query.filter_by(
            user_id=user_id).all()

        list_book_id = list(map(lambda x: x.book_id, recommend_info_origin))

        user_rating_list = BookRating.query.filter(
            and_(BookRating.user_id == user_id, BookRating.rating > 0)).all()

        update_rating = {
            user.book_id: user.rating for user in user_rating_list}

        recommend_info = list(map(lambda x: x.get_data(
            ['book_id', 'genre_weight']), recommend_info_origin))

        for idx, info in enumerate(recommend_info):
            rated = update_rating.get(info['book_id'], None)
            if rated:
                info['genre_weight'] = rated

        y = list(map(lambda x: x['genre_weight'], recommend_info))

        model = DecisionTreeRegressor(random_state=12)
        model.fit(X, y)

        y_pred = model.predict(X).tolist()
        score = model.score(X, y)

        for idx in range(len(recommend_info_origin)):
            recommend_info_origin[idx].genre_weight = y_pred[idx]
        db.session.commit()

        list_book_final = [book_id for weight, book_id in sorted(
            zip(y_pred, list_book_id), reverse=True, key=lambda x: x[0])][:LIMIT_BOOK]
        weighted_rating = BookReview.query.filter(BookReview.book_id.in_(list_book_final)).with_entities(BookReview.weighted_rating).all()

        list_book = Book.query.filter(Book.id.in_(list_book_final)).all()
        list_book = list(map(lambda x: x.get_data(['id', 'image_url', 'title']), list_book))

        list_book = [dict(item, rating=rating[0]) for item, rating in zip(list_book, weighted_rating)]


    except Exception as e:
        return make_response(make_data(dict(error=str(e)), msg="Return list recommend books by genre fail!", status='FAILURE'))

    return make_response(make_data(dict(list_book=list_book), msg="Return list recommend books by genre successfully!"))


@app.route('/api/get-some-book-similar-at-all/<int:user_id>', methods=['GET'])
def get_some_book_similar_at_all(user_id: int):
    LIMIT_BOOK = 30

    try:
        book_similar_id = BookRating.query.filter_by(
            user_id=user_id).with_entities(BookRating.book_id).all()
        book_similar_id = list(map(lambda x: x[0], book_similar_id))

        book_similar_id = BookDescriptionSimilarities.query.filter(
            BookDescriptionSimilarities.book_id.in_(book_similar_id)
        ).with_entities(
            BookDescriptionSimilarities.book_recommend_id
        ).all()

        book_similar_id = list(map(lambda x: x[0], book_similar_id))

        # choose random min(LIMIT_BOOK, len(book_similar_id))
        book_similar_id = np.random.choice(
            book_similar_id, size=min(LIMIT_BOOK, len(book_similar_id))).tolist()

        list_book = Book.query.filter(Book.id.in_(book_similar_id)).all()

        list_book = list(map(lambda x: x.get_data(['id', 'image_url', 'title']), list_book))
        weighted_rating = BookReview.query.filter(BookReview.book_id.in_(book_similar_id)).with_entities(BookReview.weighted_rating).all()

        list_book = [dict(item, rating=rating[0]) for item, rating in zip(list_book, weighted_rating)]

    except Exception as e:
        return make_response(make_data(dict(error=str(e)), msg="Return top similar book fail!", status='FAILURE'))

    return make_response(make_data(dict(list_book=list_book), msg="Return top similar book successfully!"))


@app.route('/api/get-one-top-book', methods=['GET'])
def get_one_top_book():
    try:
        book_rating = db.session.query(BookRating.book_id).all()
        book_rating = list(map(lambda x: x[0], book_rating))
        top_book_id = Counter(book_rating).most_common(1)[0][0]

    except Exception as e:
        return make_response(make_data(dict(error=str(e)), msg="Return top one book fail!", status='FAILURE'))

    return get_book(top_book_id)