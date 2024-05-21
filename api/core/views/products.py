#!/usr/bin/python3
"""
product Views module
"""
from flask_restful import Resource
import models
from ..serializers.products import ProductSchema
from marshmallow import ValidationError, EXCLUDE
from flask import request, jsonify, make_response
from utilities.auth_utils import auth_required
from datetime import datetime


product_schema = ProductSchema(unknown=EXCLUDE)
products_schema = ProductSchema(many=True)


class ProductHubList(Resource):
    """Defines get(for all) and post request of products"""
    def get(self, hub_id):
        """retrieve all products from the storage
        Arg:
            hub_id: the hub to which the product belongs
        """
        hub = models.storage.get(models.Hub, id=hub_id)
        products = hub.products
        return (products_schema.dump(products), 200)

    @auth_required(roles=['is_farmer', 'is_admin'])
    def post(self, hub_id):
        """Add a product to the storage
        Arg:
            hub_id: the hub to which the product belongs
        """
        try:
            data = request.get_json()
            data['hub_id'] = hub_id
            data = product_schema.load(data)
        except ValidationError as e:
            responseobject = {
                "status": "fail",
                "message": e.messages
            }
            return make_response(jsonify(responseobject), 400)
        new_product = models.Product(**data)
        new_product.save()
        return (product_schema.dump(new_product), 201)


class ProductSingle(Resource):
    """Retrieves a single product, deletes a product
        and makes changes to an exisiting product
    """
    def get(self, product_id):
        """retrive a single product from the storage
        Arg:
            product_id: ID of the product to retrieve
        """
        product = models.storage.get(models.Product, id=product_id)
        if product:
            return (product_schema.dump(product), 200)

    @auth_required(roles=['is_farmer', 'is_admin'])
    def delete(self, product_id):
        """Delete product
        Arg:
            product_id: ID of the product to be deleted
        """
        product = models.storage.get(models.Product, id=product_id)
        if product:
            models.storage.delete(product)
            response = {'message': 'resource successfully deleted'}
            return make_response(jsonify(response), 200)

    @auth_required(roles=["is_farmer", "is_admin"])
    def put(self, product_id):
        """Make changes to an existing product
        Arg:
            product_id: ID of the product to be changed
        """
        try:
            data = request.get_json()
            data = product_schema.load(data)
        except ValidationError as e:
            responseobject = {
                "status": "Input data invalid",
                "message": e.messages
            }
            return make_response(jsonify(responseobject), 400)
        product = models.storage.get(models.Product, id=product_id)
        if product:
            for key in data.keys():
                if hasattr(product, key):
                    setattr(product, key, data[key])
            product.updated_at = datetime.now()
            models.storage.save()
            return (product_schema.dump(product), 200)


class ProductCategoryList(Resource):
    """Defines get(for all) and post request of products"""
    def get(self, cat_id):
        """retrieve all products from the storage
        related to a particular category
        Arg:
            cat_id: the hub to which the product belongs"""
        cat = models.storage.get(models.Category, id=cat_id)
        products = cat.products
        return (products_schema.dump(products), 200)
