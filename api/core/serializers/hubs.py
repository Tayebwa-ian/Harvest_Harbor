#!/usr/bin/python3
"""HubSchema - Module
"""
from marshmallow import Schema, fields
from enum import Enum


class Status(Enum):
    """Define possible statuses of a Hub"""
    ACTIVE = 'active'
    APPROVED = 'approved'
    PENDING = 'pending'
    SUSPENDED = 'suspended'


class Rank(Enum):
    """Define possible ranks of a Hub"""
    REGULAR = 'regular'
    STAR = 'star'
    DIAMOND = 'diamond'


class HubSchema(Schema):
    """A hub schema
    Responsible for: -serialization/deserialization
                     -Data validation
                     -add data to the hubs table
                     using the load method and the post_load decorator
    """
    id = fields.Str(dump_only=True)
    created_at = fields.Str(dump_only=True)
    updated_at = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    is_bulk_seller = fields.Bool()
    is_retailer = fields.Bool()
    status = fields.Enum(Status)
    rank = fields.Enum(Rank)
    location_id = fields.Str(required=True)
    owner_id = fields.Str(required=True)
