#!/usr/bin/python3
"""Product Model-Module(Inherits from the BaseModel)"""
from .base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import String, Column, ForeignKey, Integer, Float, Boolean


class Product(BaseModel, Base):
    """Holds Review attributes and Functions
    Attrs:
        name: product name
        description: the product described
        sell_volume: name of the sell volume of the product eg boxes
        quantities: available quantities of the sell volume
        unit_price: price of each sell volume
        is_default: the default/main location of a user (it can be changed)
        hub_id: ID of the hub to which the product belongs
        cat_id: ID of the category to which the product belongs
    """
    __tablename__ = 'products'
    name = Column(String(128), nullable=False)
    description = Column(String(256), nullable=False)
    sell_volume = Column(String(128), nullable=False)
    quantities = Column(Integer, default=0)
    unit_price = Column(Float, default=0.0)
    is_default = Column(Boolean, default=False)
    hub_id = Column(String(60), ForeignKey("hubs.id"), nullable=False)
    cat_id = Column(String(60), ForeignKey("categories.id"), nullable=False)
    sales = relationship("Sale", backref="product")
    reviews = relationship("Review", backref="product", cascade="delete")
    images = relationship("Image", backref="product", cascade="delete")

    def __init__(self, *args, **kwargs):
        """initializes Product class"""
        super().__init__(*args, **kwargs)
