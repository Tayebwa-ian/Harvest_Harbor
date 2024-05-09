#!/usr/bin/python3
"""create a unique Storage instance for the application"""
from .engine import db_storage
from .base_model import BaseModel
from .categories import Category
from .hubs import Hub
from .images import Image
from .sales import Sale
from .reviews import Review
from .users import User, BlacklistToken
from .locations import Location
from .products import Product
from os import getenv


# load from database
db = getenv('HH_MYSQL_DB')
if db:
    storage = db_storage.DBStorage()
    storage.reload()
