#!/usr/bin/python3
"""SoldProductSchema - Module
"""
from marshmallow import Schema, fields, ValidationError, validates
from flask import request
import models


class SoldProductSchema(Schema):
    """A Sold product schema
    Responsible for: -serialization/deserialization
                     -Data validation
                     -add data to the sold_products table
                     using the load method and the post_load decorator
    """
    id = fields.Str(dump_only=True)
    created_at = fields.Str(dump_only=True)
    updated_at = fields.Str(dump_only=True)
    product_id = fields.Str(required=True)
    purchase_id = fields.Str(required=True)
    unit_price = fields.Float()
    quantities = fields.Integer()

    @validates('quantities')
    def validate_quantities(self, value) -> None:
        """set the input value of the quantities to 1 if it is empty
        and check quantities is not more than what is existing
        Arg:
            value: input value
        """
        methods = ['POST', 'PUT']
        product = models.storage.get(models.Product, id=self.product_id)
        if request.method in methods and value == None:
            value = 1
        elif request.method in methods and(self.quantities >
                                           product.quantities):
            raise ValidationError(
                f"quantities must be equal to\
                    or less than {product.quantities}"
            )
        # Reduce product quantities according to the request made
        if request.method in methods:
            product.quantities -= value
            models.storage.save()

    @validates('unit_price')
    def validate_unit_price(self, value):
        """Ensure unit price is not empty
        Arg:
            value: input value
        """
        methods = ['POST', 'PUT']
        if request.method in methods and value == None:
            raise ValidationError(
                "Unit price field can not be empty"
            )
