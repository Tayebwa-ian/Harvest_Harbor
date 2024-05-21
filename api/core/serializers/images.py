#!/usr/bin/python3
"""ImageSchema - Module
"""
from marshmallow import Schema, fields, validates, ValidationError
import models


class ImageSchema(Schema):
    """A Image schema
    Responsible for: -serialization/deserialization
                     -Data validation
    """
    id = fields.Str(dump_only=True)
    created_at = fields.Str(dump_only=True)
    updated_at = fields.Str(dump_only=True)
    link = fields.Str(required=True)
    product_id = fields.Str()
    hub_id = fields.Str()

    @validates('link')
    def validate_link(self, value) -> None:
        """Validate the input value of the link field
        Ensure no Image exists in the storage with the same link
        Arg:
            value: input value
        """
        if models.storage.get(models.Image, link=value):
            raise ValidationError(f'Image with name {value} already exists')
