#!/usr/bin/python3
"""UserSchema - Module
"""
from marshmallow import Schema, fields, validates, ValidationError
import models


class UserSchema(Schema):
    """A User schema
    Responsible for: -serialization/deserialization
                     -Data validation
                     -add data to the users table
                     using the load method and the post_load decorator
    """
    id = fields.Str(dump_only=True)
    created_at = fields.Str(dump_only=True)
    updated_at = fields.Str(dump_only=True)
    email = fields.Str(required=True)
    username = fields.Str(required=True)
    password = fields.Str(load_only=True, required=True)
    phone_number = fields.Str(required=True)
    is_farmer = fields.Bool()
    has_store = fields.Bool()
    is_bulk_buyer = fields.Bool()
    is_support = fields.Bool()
    is_admin = fields.Bool()
    is_carrier = fields.Bool()
    is_market_expert = fields.Bool()
    is_farming_expert = fields.Bool()
    status = fields.Str()

    @validates('email')
    def validate_email(self, value) -> None:
        """Validate the input value of the email field
        Ensure no user exists in the storage with the same email
        Arg:
            value: input value
        """
        if models.storage.get(models.User, email=value):
            raise ValidationError(f'Email {value} already exists')

    @validates('phone_number')
    def validate_phone_number(self, value) -> None:
        """Validate the input value of the phone_number field
        Ensure no user exists in the storage with the same phone_number
        Arg:
            value: input value
        """
        if models.storage.get(models.User, phone_number=value):
            raise ValidationError(f'phone number {value} already exists')

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
