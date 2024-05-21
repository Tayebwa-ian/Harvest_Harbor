#!/usr/bin/python3
"""
review Views module
"""
from flask_restful import Resource
import models
from ..serializers.reviews import ReviewSchema
from marshmallow import ValidationError, EXCLUDE
from flask import request, jsonify, make_response
from utilities.auth_utils import auth_required, get_current_user
from datetime import datetime


review_schema = ReviewSchema(unknown=EXCLUDE)
reviews_schema = ReviewSchema(many=True)


class ReviewProductList(Resource):
    """Defines get(for all) and post request of reviews"""
    def get(self, product_id):
        """retrieve all reviews from the storage"""
        product = models.storage.get(models.Product, id=product_id)
        reviews = product.reviews
        return (reviews_schema.dump(reviews), 200)

    @auth_required()
    def post(self, product_id):
        """Add a review to the storage"""
        user = get_current_user()
        try:
            data = request.get_json()
            data['product_id'] = product_id
            data['owner_id'] = user.id
            data = review_schema.load(data)
        except ValidationError as e:
            responseobject = {
                "status": "fail",
                "message": e.messages
            }
            return make_response(jsonify(responseobject), 400)
        new_review = models.Review(**data)
        new_review.save()
        return (review_schema.dump(new_review), 201)


class ReviewSingle(Resource):
    """Retrieves a single review, deletes a review
        and makes changes to an exisiting review
    """
    def get(self, review_id):
        """retrive a single review from the storage
        Arg:
            review_id: ID of the review to retrieve
        """
        review = models.storage.get(models.Review, id=review_id)
        if review:
            return (review_schema.dump(review), 200)

    @auth_required()
    def delete(self, review_id):
        """Delete review
        Arg:
            review_id: ID of the review to be deleted
        """
        user = get_current_user()
        review = models.storage.get(models.Review, id=review_id)
        if review.owner_id == user.id:
            models.storage.delete(review)
            response = {'message': 'resource successfully deleted'}
            return make_response(jsonify(response), 200)

    @auth_required()
    def put(self, review_id):
        """Make changes to an existing review
        Arg:
            review_id: ID of the review to be changed
        """
        user = get_current_user()
        try:
            data = request.get_json()
            data['owner_id'] = user.id
            data = review_schema.load(data)
        except ValidationError as e:
            responseobject = {
                "status": "Input data invalid",
                "message": e.messages
            }
            return make_response(jsonify(responseobject), 400)
        review = models.storage.get(models.Review, id=review_id)
        if review.owner_id == user.id:
            for key in data.keys():
                if hasattr(review, key):
                    setattr(review, key, data[key])
            review.updated_at = datetime.now()
            models.storage.save()
            return (review_schema.dump(review), 200)
