#!/usr/bin/python3
"""
category Views module
"""
from flask_restful import Resource
from models import storage, Product
from ..serializers.products import ProductSchema
from marshmallow import ValidationError, EXCLUDE
from flask import request, abort
import json


product_schema = ProductSchema(unknown=EXCLUDE)
products_schema = ProductSchema(many=True)


class ProductList(Resource):
    """Defines get(for all) and post request of products"""
    def get(self):
        """retrieve all categories from the storage"""
        products = storage.all(Product)
        return (products_schema.dump(products), 200)

    def post(self):
        """Add a product to the storage"""
        try:
            data = product_schema.load(request.get_json())
        except ValidationError as e:
            abort(400, "invalid input data")
        new_product = Product(**data)
        new_product.save()
        return (product_schema.dump(new_product), 201)


class ProductSingle(Resource):
    """Retrieves a single product, deletes a product
        and makes changes to an exisiting product
    Arg:
        product_name: name of the category to retrieve
    """
    def get(self, product_name):
        """retrive a single product from the storage"""
        product = storage.get(Product, name=product_name)
        if product:
            return (product_schema.dump(product), 200)

    def delete(self, product_name):
        """Delete product
        Arg:
            product_name: name of the product to be deleted
        """
        product = storage.get(Product, name=product_name)
        if product:
            storage.delete(product)
            response = {'message': 'resource successfully deleted'}
            return (json.dumps(response), 204)

    def put(self, product_name):
        """Make changes to an existing product
        Arg:
            product_name: name of the product to be changed
        """
        try:
            data = product_schema.load(request.get_json())
        except ValidationError as e:
            abort(400, "invalid input data")
        product = storage.get(Product, id=product_name)
        if product:
            for key in data.keys():
                if hasattr(product, key):
                    setattr(product, data[key])
            storage.save()
            return (product_schema.dump(product), 200)
