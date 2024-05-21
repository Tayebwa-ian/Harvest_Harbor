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
core_api.add_resource(HubList, '/hubs')
core_api.add_resource(HubSingle, '/hubs/<hub_id>')
core_api.add_resource(ImageHubList, '/<hub_id>/hubimages')
core_api.add_resource(ImageProductList, '/<product_id>/productimages')
core_api.add_resource(ImageSingle, '/images/<image_id>')
core_api.add_resource(LocationHubList, '/<hub_id>/locations')
core_api.add_resource(LocationUserList, '/locations')
core_api.add_resource(LocationSingle, '/locations/<location_id>')
core_api.add_resource(ProductHubList, '/<hub_id>/products')
core_api.add_resource(ProductCategoryList, '/<cat_id>/products')
core_api.add_resource(ProductSingle, '/products/<product_id>')
core_api.add_resource(ReviewProductList, '/<product_id>/reviews')
core_api.add_resource(ReviewSingle, '/reviews/<review_id>')
core_api.add_resource(CartProducts, '/<cart_id>/cart_products')
core_api.add_resource(CartProductsSingle, '/cart_products/<sold_pdt_id>')
core_api.add_resource(UserPurchasesList, '/purchases')
