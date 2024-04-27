#!/usr/bin/python3
"""CategorySchema - Module
"""
from marshmallow import Schema, fields, post_load
from models import Category


class CategorySchema(Schema):
    """A category schema
    Responsible for: -serialization/deserialization
                     -Data validation
                     -add data to the categories table
                     using the load method and the post_load decorator
    """
    id = fields.Str(dump_only=True)
    created_at = fields.Str(dump_only=True)
    updated_at = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    category_id = fields.Str()

    @post_load
    def create_category(self, data, **kwargs) -> None:
        """create a category instance in the categories table
            when the loads method is called on this class and data is valid
        Args:
            data: the validated request data
            kwargs: any other key word arguments
        """
        return (Category(**data))
