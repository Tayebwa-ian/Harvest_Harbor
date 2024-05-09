#!/usr/bin/python3
"""productSchema - Module
"""
from marshmallow import Schema, fields


class ProductSchema(Schema):
    """A Product schema
    Responsible for: -serialization/deserialization
                     -Data validation
                     -add data to the products table
                     using the load method and the post_load decorator
    """
    id = fields.Str(dump_only=True)
    created_at = fields.Str(dump_only=True)
    updated_at = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    sell_volume = fields.Str(required=True)
    quantities = fields.Float()
    unit_price = fields.Float()
    cat_id = fields.Str(required=True)
    hub_id = fields.Str(required=True)
