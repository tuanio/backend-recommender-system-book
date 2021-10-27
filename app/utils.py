from flask import jsonify

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
