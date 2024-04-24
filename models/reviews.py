#!/usr/bin/python3
"""Review Model-Module(Inherits from the BaseModel)"""
from .base_model import BaseModel, Base
from sqlalchemy import String, Column, ForeignKey


class Review(BaseModel, Base):
    """Holds Review attributes and Functions
    Attrs:
        text: review message
        owner_id: ID of the reviewer
        product_id: ID of the product the review belongs to
    """
    __tablename__ = 'reviews'
    text = Column(String(256), nullable=False)
    owner_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    product_id = Column(String(60), ForeignKey("products.id"), nullable=False)

    def __init__(self, *args, **kwargs):
        """initializes Review class"""
        super().__init__(*args, **kwargs)
