from flask import request, jsonify, make_response
from functools import wraps


def validate_bouquet_adding(func):
    """Decorator to validate the addition of a bouquet"""

    @wraps(func)
    def wrapper():
        if func.__name__ == 'post':
            request_data = request.get_json()
            try:
                for key, value in request_data.items():
                    if key != 'should_refresh':
                        if value.isspace() or len(value) < 1:
                            return make_response(jsonify({"error": f'{key} should have at least one character'}), 400)
                if type(request_data['bouquet_name']) == int:
                    return make_response(jsonify({"error": "bouquet name should not be numeric"}), 400)
                elif request_data['bouquet_name'].isspace() or len(request_data['bouquet_name']) < 1:
                    return make_response(jsonify({"error": "bouquet name should have at least one character"}), 400)
                else:
                    return func()
            except KeyError as error:
                return make_response(jsonify({"error": f'please provide {error}'}), 400)
            # except:
            #     return make_response(jsonify({"error": "failed to add bouquet"}), 500)
        return func()

    return wrapper
