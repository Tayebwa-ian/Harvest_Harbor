#!/usr/bin/python3
"""Project utilities Module"""
from flask import request, make_response, jsonify, g
import models
from functools import wraps


def check_roles(roles, user_obj) -> bool:
    """Checks if the user fullfills certain roles
    Args:
        roles: a list of roles allowed to access a particular endpoint
        user_obj: the user object to check for the roles
    """
    for role in roles:
        if getattr(user_obj, role, None):
            return True
    return False

def auth_required(roles=[]):
    """checks if the user is authentic
    Arg:
        roles: list of roles assigned to a specific user
    """
    def inner_function(func, *args, **kwargs):
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
                        if len(roles) > 0 and check_roles(roles, user):
                            # storing user object in g for future use
                            g.user = user
                            return func(*args, **kwargs)
                        elif len(roles) == 0:
                            # storing user object in g for future use
                            g.user = user
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

def get_current_user() -> object:
    """Retrieve current user from global object
    Return: a user object or None
    """
    try:
        user = g.user
    except AttributeError as e:
        return None
    return user
