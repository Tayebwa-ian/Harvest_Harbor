#!/usr/bin/python3
"""UserSchema - Module
"""
from marshmallow import Schema, fields, post_load, validates, ValidationError
from models import User, storage
from enum import Enum


class Status(Enum):
    """Define possible statuses of a Hub"""
    ACTIVE = 'active'
    APPROVED = 'approved'
    PENDING = 'pending'
    SUSPENDED = 'suspended'


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
    phone_number = fields.Str(required=True)
    is_farmer = fields.Bool()
    has_store = fields.Bool()
    is_bulk_buyer = fields.Bool()
    is_support = fields.Bool()
    is_admin = fields.Bool()
    is_carrier = fields.Bool()
    is_market_expert = fields.Bool()
    is_farming_expert = fields.Bool()
    status = fields.Enum(Status)

    @validates('email')
    def validate_email(self, value) -> None:
        """Validate the input value of the email field
        Ensure no user exists in the storage with the same email
        Arg:
            value: input value
        """
        if storage.get(User, email=value):
            raise ValidationError('Email already exists')

    @validates('phone_number')
    def validate_phone_number(self, value) -> None:
        """Validate the input value of the phone_number field
        Ensure no user exists in the storage with the same phone_number
        Arg:
            value: input value
        """
        if storage.get(User, phone_number=value):
            raise ValidationError('phone number already exists')

    @post_load
    def create_user(self, data, **kwargs) -> None:
        """create a user instance in the users table
            when the loads method is called on this class and data is valid
        Args:
            data: the validated request data
            kwargs: any other key word arguments
        """
        return (User(**data))
