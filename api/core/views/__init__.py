#!/usr/bin/python3
"""
Core Views module Initiation
"""
from flask_restful import Api
from flask import Blueprint


core_bp = Blueprint('core_bp', __name__, url_prefix="/api/core")
core_api = Api(core_bp)

from .categories import *
from .hubs import *
from .images import *
from .locations import *
from .products import *
from .reviews import *
from .sales import *

core_api.add_resource(CategoryList, '/categories')
core_api.add_resource(CategorySingle, '/categories/<cat_id>')
