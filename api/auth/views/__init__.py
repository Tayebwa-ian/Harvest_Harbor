#!/usr/bin/python3
"""
Auth Views module Initiation
"""
from flask_restful import Api
from flask import Blueprint


auth_bp = Blueprint('auth_bp', __name__, url_prefix="/api/auth")
auth_api = Api(auth_bp)

from .users import *

auth_api.add_resource(RegisterUser, '/register')
auth_api.add_resource(LoginUser, '/login')
auth_api.add_resource(UserStatus, '/status')
auth_api.add_resource(LogoutUser, '/logout')
