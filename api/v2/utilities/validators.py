from functools import wraps

from cerberus import Validator
from validator_collection import checkers
from flask import request, jsonify, make_response

from api.v2.helpers.credentials import check_bouquet_credentials


def validate_bouquet_adding(func):
    """Decorator to validate the addition of a bouquet"""

    @wraps(func)
    def wrapper():
        if func.__name__ == 'post':
            try:
                data = request.get_json()
                schema = {
                    'bouquet_name': {'type': 'string', 'empty': False},
                    'client_id': {'type': 'string', 'empty': False},
                    'client_secret': {'type': 'string', 'empty': False},
                    'token_uri': {'type': 'string', 'empty': False},
                    'auth_uri': {'type': 'string', 'empty': False},
                    'redirect_uris': {'type': ['string', 'list'], 'empty': False},
                    'refresh_url': {'type': 'string'},
                    'should_refresh': {'type': 'boolean'},
                    'refresh_token': {'type': 'string', 'empty': False}
                }
                v = Validator()
                is_valid = v.validate(data, schema)
                if not is_valid:
                    return make_response(jsonify({'errors': v.errors}), 400)
                elif 'refresh_url' in data.keys() and not checkers.is_url(data['refresh_url']):
                    return make_response(jsonify({"error": "please provide a valid url e.g 'https://re.com'"}), 400)
                return func()
            except KeyError as error:
                return make_response(jsonify({'error': f'please provide {error}'}), 400)
            except:
                return make_response(jsonify({'error': 'failed to add bouquet'}), 500)
        return func()
    return wrapper
