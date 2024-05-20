#!/usr/bin/python3
"""
user Views module
"""
from flask_restful import Resource
import models
from ..serializers.users import UserSchema
from marshmallow import ValidationError, EXCLUDE
from flask import request
from flask import jsonify, make_response
import api


user_schema = UserSchema(unknown=EXCLUDE)


class RegisterUser(Resource):
    """Defines user registration mechanism"""

    def post(self):
        """Add a user to the storage"""
        try:
            data = request.get_json()
            data = user_schema.load(data)
        except ValidationError as e:
            responseObject = {
                'status': 'fail',
                'message': e.messages
            }
            return make_response(jsonify(responseObject), 202)
        new_user = models.User(**data)
        new_user.save()
        responseObject = {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "phone_number": new_user.phone_number,
            "is_admin": new_user.is_admin,
        }
        return make_response(jsonify(responseObject), 201)


class LoginUser(Resource):
    """Deifnes how user gets into the system"""

    def post(self):
        """Add a user to the storage"""
        data = request.get_json()
        email = data.get('email')
        user = models.storage.get(models.User, email=email)
        if user and api.app.bcrypt.check_password_hash(
             user.password, data.get('password')):
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                responseObject = {
                    "status": "success",
                    "message": "Successfully Logged in",
                    "auth_token": auth_token,
                }
                return make_response(jsonify(responseObject), 200)
        else:
            responseObject = {
                "status": "fail",
                "message": "wrong credentials provided",
            }
            return make_response(jsonify(responseObject), 401)


class UserStatus(Resource):
    """Defines the status of a user"""

    def get(self):
        """Retreive info about a specific user"""
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
                    return (user_schema.dump(user), 200)
            responseObject = {
                'status': 'fail',
                'message': resp
            }
            return make_response(jsonify(responseObject), 401)
        else:
            responseObject = {
                'status': 'fail',
                'message': 'auth token is invalid.'
            }
            return make_response(jsonify(responseObject), 401)


class LogoutUser(Resource):
    """Defines how the user gets out of the system"""

    def post(self):
        """Logout a logged in user"""
        # get auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = models.User.decode_auth_token(auth_token)
            if isinstance(resp, str):
                # mark the token as blacklisted
                blacklist_token = models.BlacklistToken(token=auth_token)
                blacklist_token.save()
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully logged out.'
                }
                return make_response(jsonify(responseObject), 200)
            else:
                responseObject = {
                    'status': 'fail',
                    'message': resp
                }
                return make_response(jsonify(responseObject), 401)
        else:
            responseObject = {
                'status': 'fail',
                'message': 'auth token is invalid.'
            }
            return make_response(jsonify(responseObject), 403)
