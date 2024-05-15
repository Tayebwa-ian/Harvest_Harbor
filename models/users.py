#!/usr/bin/python3
"""User Model-Module(Inherits from the BaseModel)"""
from .base_model import BaseModel, Base
from sqlalchemy import String, Column, Boolean, Enum
from sqlalchemy.orm import relationship
from api.app import bcrypt
import jwt
from os import getenv
import datetime
import models


if getenv('SECRET_KEY'):
    secret_key = getenv('SECRET_KEY')
else:
    secret_key = b'''\xb1KW\x82\xea\x06\xeb\xd2\xde\xb20L
    \xa4y\xd3\xb0\x92\xd8\xdb\xb9\xf6\x91\x98\xd0'''


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
    __tablename__ = "users"
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    username = Column(String(128), nullable=False)
    phone_number = Column(String(128), nullable=False, unique=True)
    is_farmer = Column(Boolean, default=False)
    has_store = Column(Boolean, default=False)
    is_bulk_buyer = Column(Boolean, default=False)
    is_support = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    is_carrier = Column(Boolean, default=False)
    is_market_expert = Column(Boolean, default=False)
    is_farming_expert = Column(Boolean, default=False)
    status = Column(String(56), Enum("acitve", "suspended"),
                    default="active")
    reviews = relationship("Review", backref="owner", cascade="delete")
    hubs = relationship("Hub", backref="owner", cascade="delete")
    sales = relationship("Sale", backref="owner", cascade="delete")
    locations = relationship("Location", backref="owner", cascade="delete")

    def __init__(self, *args, **kwargs):
        """initializes Product class"""
        if kwargs:
            kwargs['password'] = bcrypt.generate_password_hash(
                kwargs['password']).decode()
        super().__init__(*args, **kwargs)

    def encode_auth_token(self, user_id) -> str:
        """
        Generates the Auth Token
        Arg:
            user_id: ID of the user whose token should be generated
        return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.now() +
                datetime.timedelta(days=0, seconds=900),
                'iat': datetime.datetime.now(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                key=secret_key,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token) -> str:
        """
        Validates the auth token
        param:
            auth_token - token to decode
        """
        try:
            payload = jwt.decode(auth_token, key=secret_key,
                                 algorithms=['HS256'])
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class BlacklistToken(BaseModel, Base):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    token = Column(String(500), unique=True, nullable=False)

    def __init__(self, *args, **kwargs):
        """Intialize the BlacklistToken class
        """
        super().__init__(*args, **kwargs)

    @staticmethod
    def check_blacklist(auth_token) -> bool:
        """check whether auth token has been blacklisted"""
        res = models.storage.get(BlacklistToken, token=auth_token)
        if res:
            return True
        else:
            return False
