#!/usr/bin/python3
"""productSchema - Module
"""
from marshmallow import Schema, fields, post_load
from models import Product


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

    @post_load
    def create_location(self, data, **kwargs) -> None:
        """create a product instance in the products table
            when the loads method is called on this class and data is valid
        Args:
            data: the validated request data
            kwargs: any other key word arguments
        """
        return (Product(**data))
