#!/usr/bin/python3
"""
Auth Views module Initiation
"""
from flask_restful import Api
from flask import Blueprint


auth_bp = Blueprint('core_bp', __name__, url_prefix="/api/auth")
auth_api = Api(auth_bp)

from users import *
