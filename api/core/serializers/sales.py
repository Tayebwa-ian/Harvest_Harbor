#!/usr/bin/python3
"""SaleSchema - Module
"""
from marshmallow import Schema, fields, post_load
from models import Sale


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

    @post_load
    def create_sale(self, data, **kwargs) -> None:
        """create a sale instance in the sales table
            when the loads method is called on this class and data is valid
        Args:
            data: the validated request data
            kwargs: any other key word arguments
        """
        return (Sale(**data))
