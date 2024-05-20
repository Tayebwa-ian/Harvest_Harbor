#!/usr/bin/python3
"""
category Views module
"""
from flask_restful import Resource
import models
from ..serializers.categories import CategorySchema
from marshmallow import ValidationError, EXCLUDE
from flask import request, jsonify, make_response
from utilities.auth_utils import auth_required
from datetime import datetime


category_schema = CategorySchema(unknown=EXCLUDE)
categories_schema = CategorySchema(many=True)


class CategoryList(Resource):
    """Defines get(for all) and post request of categories"""
    def get(self):
        """retrieve all categories from the storage"""
        categories = models.storage.all(models.Category)
        return (categories_schema.dump(categories), 200)

    @auth_required(roles=["is_admin", "is_farmer"])
    def post(self):
        """Add a category to the storage"""
        try:
            data = request.get_json()
            data = category_schema.load(data)
        except ValidationError as e:
            responseobject = {
                "status": "fail",
                "message": e.messages
            }
            return make_response(jsonify(responseobject), 400)
        new_category = models.Category(**data)
        new_category.save()
        return (category_schema.dump(new_category), 201)


class CategorySingle(Resource):
    """Retrieves a single category, deletes a category
        and makes changes to an exisiting category
    """
    def get(self, cat_id):
        """retrive a single category from the storage
        Arg:
            cat_id: ID of the category to retrieve
        """
        category = models.storage.get(models.Category, id=cat_id)
        if category:
            return (category_schema.dump(category), 200)

    @auth_required(roles=["is_admin", "is_farmer"])
    def delete(self, cat_id):
        """Delete category
        Arg:
            cat_id: ID of the category to be deleted
        """
        category = models.storage.get(models.Category, id=cat_id)
        if category:
            models.storage.delete(category)
            response = {'message': 'resource successfully deleted'}
            return make_response(jsonify(response), 200)

    @auth_required(roles=["is_admin", "is_farmer"])
    def put(self, cat_id):
        """Make changes to an existing category
        Arg:
            cat_id: ID of the category to be changed
        """
        try:
            data = request.get_json()
            data = category_schema.load(data)
        except ValidationError as e:
            responseobject = {
                "status": "Input data invalid",
                "message": e.messages
            }
            return make_response(jsonify(responseobject), 400)
        category = models.storage.get(models.Category, id=cat_id)
        if category:
            for key in data.keys():
                if hasattr(category, key):
                    setattr(category, key, data[key])
            category.updated_at = datetime.now()
            models.storage.save()
            return (category_schema.dump(category), 200)
