from flask import jsonify
from app import engine_container


def make_response(data={}, status=200):
    '''
        - Make a resionable response with header
        - status default is 200 mean ok
    '''
    res = jsonify(data)
    res.headers.add('Access-Control-Allow-Origin', '*')
    res.headers.add('Content-Type', 'application/json')
    res.headers.add('Accept', 'application/json')
    return res


def cleanup(session):
    """
    This method cleans up the session object and also closes the connection pool using the dispose method.
    """
    session.close()
    engine_container.dispose()
