#!/usr/bin/python3
"""Hub Model-Module(Inherits from the BaseModel)"""
from .base_model import BaseModel, Base
from sqlalchemy import String, Column, ForeignKey, Enum, Boolean


class Hub(BaseModel, Base):
    """Holds Hub attributes and Functions
    a primary part of the app - it is like a store where a farmner registers
    an manages items he or she intends to sell.
    Attrs:
        name: Hub's name
        description: A Hub described
        is_bulk_seller: Does the hub sell its item in bulk
        is_retailer: Does the hub retail its items
        status: a hub can be active, approved, pending or suspended
        owner_id: the owner of the hub 
        rank: a hub can have ranks according to its performance
            possible ranks are regular, star and diamond
        location_id: ID of a place where the hub is located
    """
    __tablename__ = 'hubs'
    name = Column(String(128), nullable=False)
    description = Column(String(256), nullable=False)
    is_bulk_seller = Column(Boolean, default=False)
    is_retailer = Column(Boolean, default=False)
    owner_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    status = Column(Enum("acitve", "approved", "pending", "suspended"),
                    default="pending")
    rank = Column(Enum("regular", "star", "diamond"), default="regular")
    location_id = Column(String(60), ForeignKey("locations.id"), nullable=False)

    def __init__(self, *args, **kwargs):
        """initializes Hub class"""
        super().__init__(*args, **kwargs)
