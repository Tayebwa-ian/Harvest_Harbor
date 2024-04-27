#!/usr/bin/python3
"""Image Model-Module(Inherits from the BaseModel)"""
from .base_model import BaseModel, Base
from sqlalchemy import String, Column, ForeignKey


class Image(BaseModel, Base):
    """Holds Image attributes and Functions
    This is a universal storage area of all app images
    An image can be related to a hub or a product
    Attrs:
        link: the image file link
        product_id: product to which image belongs
        hub_id: hub to which the image belongs
    """
    __tablename__ = 'images'
    link = Column(String(128), nullable=False)
    product_id = Column(String(60), ForeignKey("products.id"), nullable=True)
    hub_id = Column(String(60), ForeignKey("hubs.id"), nullable=True)

    def __init__(self, *args, **kwargs):
        """initializes Image class"""
        super().__init__(*args, **kwargs)
