#!/usr/bin/python3
"""User Model-Module(Inherits from the BaseModel)"""
from .base_model import BaseModel, Base
from sqlalchemy import String, Column, Boolean, Enum
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Holds User attributes and Functions
    Attrs:
        email: user's email address
        username: name of a specific user
        phone_number: user's phone number
        password: user's password
        is_farmer: records if user is a farmer
        has_store: records if user is a store owner
        is_bulk_buyer: records if user is bulk buyer
                        this applies for bulk offtakers like factories
        is_support: records if the user in on the support team
        is_admin: records if user is a application admin
        is_carrier: records is user is a registered delivery personal
        is_market_expert: applies if a user proves to have strong knowledge
                            of agricultural markets
        is_farming_expert: applies if a user proves to have strong technical
                            knowledge about farming
        status: status of the app user (can change according to complaince)
                possible statuses are active and pending
    """
    __tablename__ = "uusers"
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    username = Column(String(128), nullable=False)
    phone_number = Column(String(128), nullable=False)
    is_farmer = Column(Boolean, default=False)
    has_store = Column(Boolean, default=False)
    is_bulk_buyer = Column(Boolean, default=False)
    is_support = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    is_carrier = Column(Boolean, default=False)
    is_market_expert = Column(Boolean, default=False)
    is_farming_expert = Column(Boolean, default=False)
    status = Column(Enum("acitve", "suspended"),
                    default="active")
    reviews = relationship("Review", backref="owner", cascade="delete")
    hubs = relationship("Hub", backref="owner", cascade="delete")
    sales = relationship("Sale", backref="owner", cascade="delete")
    locations = relationship("Location", backref="owner", cascade="delete")

    def __init__(self, *args, **kwargs):
        """initializes Product class"""
        super().__init__(*args, **kwargs)
