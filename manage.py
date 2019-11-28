import os

from flask_script import Manager, Shell
from flask import make_response, jsonify

# local imports
from app import create_app  # noqa: E402

app = create_app(os.getenv('APP_SETTINGS') or 'default')
manager = Manager(app)


def make_shell_context():
    return dict(app=app)


manager.add_command(
    "shell", Shell(
        make_context=make_shell_context))

@app.errorhandler(404)
def route_not_found(e):
    return make_response(jsonify({
        "error": 'The URL was not found. Please check your spelling and try again'
        }), 404)

if __name__ == '__main__':
    manager.run()
