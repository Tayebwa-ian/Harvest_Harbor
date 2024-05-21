#!/usr/bin/python3
"""ReviewSchema - Module
"""
from marshmallow import Schema, fields


class ReviewSchema(Schema):
    """A Review schema
    Responsible for: -serialization/deserialization
                     -Data validation
    """
    id = fields.Str(dump_only=True)
    created_at = fields.Str(dump_only=True)
    updated_at = fields.Str(dump_only=True)
    text = fields.Str(required=True)
    owner_id = fields.Str(required=True)
    product_id = fields.Str(required=True)
