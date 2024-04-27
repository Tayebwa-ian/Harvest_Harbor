#!/usr/bin/python3
"""ImageSchema - Module
"""
from marshmallow import Schema, fields, post_load
from models import Image


class ImageSchema(Schema):
    """A Image schema
    Responsible for: -serialization/deserialization
                     -Data validation
                     -add data to the images table
                     using the load method and the post_load decorator
    """
    id = fields.Str(dump_only=True)
    created_at = fields.Str(dump_only=True)
    updated_at = fields.Str(dump_only=True)
    link = fields.Str(required=True)
    product_id = fields.Str()
    hub_id = fields.Str()

    @post_load
    def create_image(self, data, **kwargs) -> None:
        """create a image instance in the images table
            when the loads method is called on this class and data is valid
        Args:
            data: the validated request data
            kwargs: any other key word arguments
        """
        return(Image(**data))
