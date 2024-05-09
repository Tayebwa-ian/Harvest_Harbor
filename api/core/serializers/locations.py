#!/usr/bin/python3
"""LocationSchema - Module
"""
from marshmallow import Schema, fields


class LocationSchema(Schema):
    """A Location schema
    Responsible for: -serialization/deserialization
                     -Data validation
                     -add data to the locations table
                     using the load method and the post_load decorator
    """
    id = fields.Str(dump_only=True)
    created_at = fields.Str(dump_only=True)
    updated_at = fields.Str(dump_only=True)
    country = fields.Str()
    state = fields.Str()
    District = fields.Str()
    postal_code = fields.Str()
    apartment_number = fields.Str()
    description = fields.Str()
    longtitude = fields.Float()
    latitude = fields.Float()
    is_default = fields.Bool()
    onwer_id = fields.Str()
    hub_id = fields.Str()
