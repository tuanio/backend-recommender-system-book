from flask import jsonify
import sys
from app import engine_container, status_code


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


def get_subset(dictionary, keys):
    return {k: dictionary[k] for k in keys}


def make_data(data: dict=dict(), msg: str="", status: str='SUCCESS') -> dict:
    return dict(
        data=data,
        msg=msg,
        status_code=status_code[status]
    )

def write(string):
    sys.stdout.write(string + '\n')