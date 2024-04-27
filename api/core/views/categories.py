#!/usr/bin/python3
"""
category Views module
"""
from flask_restful import Resource
from models import storage, Category
from serializers.categories import CategorySchema
from marshmallow import ValidationError
from flask import request, abort
import json


category_schema = CategorySchema(unknown='EXCLUDE')
categories_schema = CategorySchema(many=True)


class CategoryList(Resource):
    """Defines get(for all) and post request of categories"""
    def get(self):
        """retrieve all categories from the storage"""
        categories = storage.all(Category)
        return (categories_schema.dump(categories), 200)

    def post(self):
        """Add a category to the storage"""
        try:
            data = category_schema.load(request.get_json())
        except ValidationError as e:
            abort(400, "invalid input data")
        new_category = Category(**data)
        new_category.save()
        return (category_schema.dump(new_category), 201)


class CategorySingle(Resource):
    """Retrieves a single category, deletes a category
        and makes changes to an exisiting category
    Arg:
        cat_id: ID of the category to retrieve
    """
    def get(self, cat_id):
        """retrive a single category from the storage"""
        category = storage.get(Category, id=cat_id)
        if category:
            return (category_schema.dump(category), 200)

    def delete(self, cat_id):
        """Delete category
        Arg:
            cat_id: ID of the category to be deleted
        """
        category = storage.get(Category, id=cat_id)
        if category:
            storage.delete(category)
            response = {'message': 'resource successfully deleted'}
            return (json.dumps(response), 204)

    def put(self, cat_id):
        """Make changes to an existing category
        Arg:
            cat_id: ID of the category to be changed
        """
        try:
            data = category_schema.load(request.get_json())
        except ValidationError as e:
            abort(400, "invalid input data")
        category = storage.get(Category, id=cat_id)
        if category:
            for key in data.keys():
                if hasattr(category, key):
                    setattr(category, data[key])
            storage.save()
            return (category_schema.dump(category), 200)
