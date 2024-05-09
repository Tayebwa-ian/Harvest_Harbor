#!/usr/bin/python3
"""SaleSchema - Module
"""
from marshmallow import Schema, fields


class SaleSchema(Schema):
    """A Sale schema
    Responsible for: -serialization/deserialization
                     -Data validation
                     -add data to the sales table
                     using the load method and the post_load decorator
    """
    id = fields.Str(dump_only=True)
    created_at = fields.Str(dump_only=True)
    updated_at = fields.Str(dump_only=True)
    owner_id = fields.Str(required=True)
    location_id = fields.Str(required=True)
