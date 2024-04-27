#!/usr/bin/python3
"""LocationSchema - Module
"""
from marshmallow import Schema, fields, post_load
from models import Location


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

    @post_load
    def create_location(self, data, **kwargs) -> None:
        """create a location instance in the locations table
            when the loads method is called on this class and data is valid
        Args:
            data: the validated request data
            kwargs: any other key word arguments
        """
        return (Location(**data))
