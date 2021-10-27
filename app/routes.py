from app import app, db
from app.utils import make_response

@app.route('/', methods=['GET'])
def index():
    return make_response(dict(msg="Hello world"))
