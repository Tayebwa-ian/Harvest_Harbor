#!/usr/bin/python3
"""
product Views module
"""
from flask_restful import Resource
import models
from ..serializers.products import ProductSchema
from marshmallow import ValidationError, EXCLUDE
from flask import request
from flask import jsonify
from utilities.auth_utils import auth_required
from datetime import datetime


product_schema = ProductSchema(unknown=EXCLUDE)
products_schema = ProductSchema(many=True)


class productList(Resource):
    """Defines get(for all) and post request of products"""
    def get(self):
        """retrieve all products from the storage"""
        products = models.storage.all(models.Product)
        return (products_schema.dump(products), 200)

    @auth_required
    def post(self):
        """Add a product to the storage"""
        try:
            data = request.get_json()
            product_schema.load(data)
        except ValidationError as e:
            responseobject = {
                "status": "fail",
                "message": e.messages
            }
            return jsonify(responseobject)
        new_product = models.product(**data)
        new_product.save()
        return (product_schema.dump(new_product), 201)


class productSingle(Resource):
    """Retrieves a single product, deletes a product
        and makes changes to an exisiting product
    Arg:
        product_id: ID of the product to retrieve
    """
    def get(self, product_id):
        """retrive a single product from the storage"""
        product = models.storage.get(models.Product, id=product_id)
        if product:
            return (product_schema.dump(product), 200)

    @auth_required
    def delete(self, product_id):
        """Delete product
        Arg:
            product_id: ID of the product to be deleted
        """
        product = models.storage.get(models.Product, id=product_id)
        if product:
            models.storage.delete(product)
            response = {'message': 'resource successfully deleted'}
            return (jsonify(response))

    @auth_required(roles=["is_farmer"])
    def put(self, product_id):
        """Make changes to an existing product
        Arg:
            product_id: ID of the product to be changed
        """
        try:
            data = request.get_json()
            product_schema.load(data)
        except ValidationError as e:
            responseobject = {
                "status": "Input data invalid",
                "message": e.messages
            }
            return jsonify(responseobject)
        product = models.storage.get(models.Product, id=product_id)
        if product:
            for key in data.keys():
                if hasattr(product, key):
                    setattr(product, key, data[key])
            product.updated_at = datetime.now()
            models.storage.save()
            return (product_schema.dump(product), 200)
