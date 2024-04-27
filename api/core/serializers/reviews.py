#!/usr/bin/python3
"""ReviewSchema - Module
"""
from marshmallow import Schema, fields, post_load
from models import Review


class ReviewSchema(Schema):
    """A Review schema
    Responsible for: -serialization/deserialization
                     -Data validation
                     -add data to the reviews table
                     using the load method and the post_load decorator
    """
    id = fields.Str(dump_only=True)
    created_at = fields.Str(dump_only=True)
    updated_at = fields.Str(dump_only=True)
    text = fields.Str(required=True)
    owner_id = fields.Str(required=True)
    product_id = fields.Str(required=True)

    @post_load
    def create_review(self, data, **kwargs) -> None:
        """create a review instance in the reviews table
            when the loads method is called on this class and data is valid
        Args:
            data: the validated request data
            kwargs: any other key word arguments
        """
        return (Review(**data))
