#!/usr/bin/python3
"""CategorySchema - Module
"""
from marshmallow import Schema, fields, ValidationError, validates
import models
from flask import request


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

    @validates('name')
    def validate_name(self, value) -> None:
        """Validate the input value of the name field
        Ensure no category exists in the storage with the same name
        Arg:
            value: input value
        """
        if request.method == "POST":
            query_object = models.storage.get(models.Category, name=value)
            if query_object and len(query_object) >= 1:
                raise ValidationError(f'{value} category already exists')
