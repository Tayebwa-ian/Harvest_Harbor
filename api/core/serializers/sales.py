#!/usr/bin/python3
"""SoldProductSchema - Module
"""
from marshmallow import Schema, fields


class SoldProductSchema(Schema):
    """A Sold product schema
    Responsible for: -serialization/deserialization
                     -Data validation
    """
    id = fields.Str(dump_only=True)
    created_at = fields.Str(dump_only=True)
    updated_at = fields.Str(dump_only=True)
    product_id = fields.Str(required=True)
    purchase_id = fields.Str(required=True)
    unit_price = fields.Float(required=True)
    quantities = fields.Integer(required=True)


class PurchaseSchema(Schema):
    """A Purchase schema
    Responsible for: -serialization/deserialization
                     -Data validation
    """
    id = fields.Str(dump_only=True)
    created_at = fields.Str(dump_only=True)
    updated_at = fields.Str(dump_only=True)
    owner_id = fields.Str(required=True)
    location_id = fields.Str()
    is_closed = fields.Bool()
    sold_products = fields.List(fields.Nested(SoldProductSchema))
