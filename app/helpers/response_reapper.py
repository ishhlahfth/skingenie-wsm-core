from flask import jsonify


def response_wrapper(data=None, code=200, message="Ok"):
    return jsonify({
        "data": data or {},
        "meta": {
            "code": code,
            "message": message
        }
    })