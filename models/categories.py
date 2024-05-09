#!/usr/bin/python3
"""Category Model-Module(Inherits from the BaseModel)"""
from .base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import String, Column, ForeignKey


class Category(BaseModel, Base):
    """Holds Category attributes and Functions
    Attrs:
        name: category's name
        description: A category described
        category_id: ID of the category in which the category falls under
    """
    __tablename__ = 'categories'
    name = Column(String(128), nullable=False, unique=True)
    description = Column(String(256), nullable=True)
    category_id = Column(String(60), ForeignKey("categories.id"),
                         nullable=True)
    products = relationship("Product", backref="category", cascade="delete")

    def __init__(self, *args, **kwargs):
        """initializes Category class"""
        super().__init__(*args, **kwargs)
