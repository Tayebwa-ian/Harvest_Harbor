#!/usr/bin/python3
"""Sale Model-Module(Inherits from the BaseModel)"""
from .base_model import BaseModel, Base
from sqlalchemy import String, Column, ForeignKey, Float, Integer, Boolean
from sqlalchemy.orm import relationship


class SoldProduct(BaseModel, Base):
    """Holds sale ID and products related to that sale
    defines many to many relationship between products and sales
    Attrs:
        product_id: ID of the sold product
        sale_id: Sale ID to which products belong
        unit_price: unit price of the product at the time the sale is made
        quantities: numbers bought
    """
    __tablename__ = 'sold_products'
    product_id = Column(String(60), ForeignKey("products.id"),
                        nullable=False)
    purchase_id = Column(String(60), ForeignKey("purchases.id"),
                         nullable=False)
    unit_price = Column(Float, nullable=False)
    quantities = Column(Integer, nullable=False)

    def __init__(self, *args, **kwargs):
        """initializes SoldProducts class"""
        super().__init__(*args, **kwargs)


class Purchase(BaseModel, Base):
    """Holds Purchase attributes and Functions
    Note: A purchase is an open cart is the is_closed attr is false
    Attrs:
        owner_id: ID of the user/customer the purchase belongs to
        location_id: ID of the place where the products are to be delivered
        is_closed: Turns true is the purchase is completed successfully
    """
    __tablename__ = 'purchases'
    owner_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    location_id = Column(String(60), ForeignKey("locations.id"))
    is_closed = Column(Boolean, default=False)
    sold_products = relationship("SoldProduct",
                                 backref="purchase", cascade="delete")

    def __init__(self, *args, **kwargs):
        """initializes Purchase class"""
        super().__init__(*args, **kwargs)
