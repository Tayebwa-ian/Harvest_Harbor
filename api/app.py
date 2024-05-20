#!/usr/bin/python3
"""
Module contain app instance
And all config necessary to run the app
"""
from flask import Flask, jsonify, g
import models
from .core.views import core_bp
from .auth.views import auth_bp
from os import getenv
from flask_cors import CORS
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.register_blueprint(core_bp)
app.register_blueprint(auth_bp)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
bcrypt = Bcrypt(app)


@app.teardown_appcontext
def teardown(self) -> None:
    """Close the storage session"""
    models.storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """json 404 page"""
    return (jsonify({"error": "Not found"}))


@app.errorhandler(400)
def handle_bad_request(error):
    """json 400 page"""
    return (jsonify({'error': 'Bad request'}))


@app.teardown_request
def teardown_request(exception=None):
    """Clean up g after each request"""
    g.pop('user', None)


if __name__ == "__main__":
    host = getenv("HH_API_HOST", "0.0.0.0")
    port = int(getenv("HH_API_PORT", "5000"))
    app.run(host, port=port, threaded=True, debug=True)
