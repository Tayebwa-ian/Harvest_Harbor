#!/usr/bin/python3
"""Sale Model-Module(Inherits from the BaseModel)"""
from .base_model import BaseModel, Base
from sqlalchemy import String, Column, ForeignKey, Float, Integer
from sqlalchemy import Table


sold_products = Table("sold_products", Base.metadata,
                      Column("product_id", String(60),
                             ForeignKey("products.id"), nullable=False),
                      Column("sale_id", String(60),
                             ForeignKey("sales.id"), nullable=False),
                      Column("unit_price", Float, nullable=False),
                      Column("quantities", Integer, nullable=False))


class Sale(BaseModel, Base):
    """Holds Sale attributes and Functions
    Attrs:
        owner_id: ID of the user/customer the sale belongs to
        location_id: ID of the place where the products are to be delivered
    """
    __tablename__ = 'sales'
    owner_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    location_id = Column(String(60), ForeignKey("locations.id"))

    def __init__(self, *args, **kwargs):
        """initializes Hub class"""
        super().__init__(*args, **kwargs)
