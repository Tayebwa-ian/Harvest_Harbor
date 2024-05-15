#!/usr/bin/python3
"""Project utilities Module"""
from flask import request, make_response, jsonify
import models
from functools import wraps


def auth_required(roles=[]):
    """checks if the user is authenticate
    Arg:
        roles: list of roles assigned to a specific user
    """
    def inner_function(func):
        """Takes the original function as an arg and pass it down"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            """Implements the authetication logic"""
            # get the auth token
            auth_header = request.headers.get('Authorization')
            if auth_header:
                try:
                    auth_token = auth_header.split(" ")[1]
                except IndexError:
                    responseObject = {
                        'status': 'fail',
                        'message': 'Bearer token malformed.'
                    }
                    return make_response(jsonify(responseObject), 401)
            else:
                auth_token = ''
            if auth_token:
                resp = models.User.decode_auth_token(auth_token)
                if isinstance(resp, str):
                    user = models.storage.get(models.User, id=resp)
                    if user:
                        if len(roles) > 0 and all(
                                getattr(user, i, None) for i in roles):
                            return func(*args, **kwargs)
                        elif len(roles) == 0:
                            return func(*args, **kwargs)
                        else:
                            responseObject = {
                                'status': 'fail',
                                'message': f'{user.username} is not ' +
                                'authorised to access this resource',
                            }
                            return make_response(jsonify(responseObject), 401)
                    else:
                        responseObject = {
                            'status': 'fail',
                            'message': 'No user with such credentials'
                        }
                        return make_response(jsonify(responseObject), 401)
                else:
                    responseObject = {
                        'status': 'Authentication fail',
                        'message': 'Invalid token'
                    }
                    return make_response(jsonify(responseObject), 401)
        return wrapper
    return inner_function
