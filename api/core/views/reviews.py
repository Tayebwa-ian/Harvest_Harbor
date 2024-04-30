#!/usr/bin/python3
"""
reviews Views module
"""
from flask_restful import Resource
from models import storage, Review
from ..serializers.reviews import ReviewSchema
from marshmallow import ValidationError, EXCLUDE
from flask import request, abort
import json


review_schema = ReviewSchema(unknown=EXCLUDE)
reviews_schema = ReviewSchema(many=True)

class ReviewList(Resource):
    """Defines get(for all) for reviews"""
    def get(self):
        """retrieve all review details from the storage"""
        reviews = storage.all(Review)
        return (review_schema.dump(reviews), 200)
    
    def post(self):
        """Add review details to the storage"""
        try:
            data = review_schema.load(request.get_json())
        except ValidationError as e:
            abort(400, "invalid input data")
        new_review = Review(**data)
        new_review.save()
        return (review_schema.dump(new_review), 201)

    """todo: get review detail for a particular product from a particular user"""

