#!/usr/bin/python3
"""HubSchema - Module
"""
from marshmallow import Schema, fields, validates, ValidationError
import models
from flask import request


class HubSchema(Schema):
    """A hub schema
    Responsible for: -serialization/deserialization
                     -Data validation
    """
    id = fields.Str(dump_only=True)
    created_at = fields.Str(dump_only=True)
    updated_at = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    is_bulk_seller = fields.Bool()
    is_retailer = fields.Bool()
    status = fields.Str()
    rank = fields.Str()
    owner_id = fields.Str(required=True)

    @validates('status')
    def validate_status(self, value) -> None:
        """Validate the input value of the status field
        Ensure status is among (active, approved, pending and suspended)
        Arg:
            value: input value
        """
        status_list = ['active', 'suspended', 'approved', 'pending']
        if value not in status_list:
            raise ValidationError(
                f'{value} not among valid statuses({status_list})')

    @validates('rank')
    def validate_rank(self, value) -> None:
        """Validate the input value of the rank field
        Ensure rank is among (regular, star, diamond)
        Arg:
            value: input value
        """
        rank_list = ['regular', 'star', 'diamond']
        if value not in rank_list:
            raise ValidationError(
                f'{value} not among valid ranks({rank_list})')

    @validates('name')
    def validate_name(self, value) -> None:
        """Validate the input value of the name field
        Ensure no Hub exists in the storage with the same name
        Arg:
            value: input value
        """
        if request.method == 'POST':
            if models.storage.get(models.Hub, name=value):
                raise ValidationError(f'Hub {value} already exists')
