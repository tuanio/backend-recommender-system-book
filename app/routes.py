from app import app, db
from app.models import *
from app.utils import make_response


@app.route('/', methods=['GET'])
def index():
    return make_response(dict(msg="Hello world"))


# @app.route('/api/book-similar/<int:book_id>')
# def book_similar(book_id: int):
#     bookBookDescriptionSimilarities.query.filter_by(book_id=book_id)