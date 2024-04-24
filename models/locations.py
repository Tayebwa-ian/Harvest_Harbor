#!/usr/bin/python3
"""Location Model-Module(Inherits from the BaseModel)"""
from .base_model import BaseModel, Base
from sqlalchemy import String, Column, ForeignKey, Float


class Location(BaseModel, Base):
    """Holds Location attributes and Functions
    Attrs:
        country: country where the place is
        state: the state where the place is
        District: of the place
        street: street name and number of the place
        postal_code: if the place has a postal code
        apartment_number: if its a apartment
        description: further description of the location
        Longtitude: coordinates
        latittude: coordinates
        owner_id: ID of owner of the location (optional)
        hub_id: ID of the hub located in this place  (optinal)

    """
    __tablename__ = "locations"
    country = Column(String(60))
    state = Column(String(60))
    District = Column(String(60))
    postal_code = Column(String(60))
    apartment_number = Column(String(60))
    description = Column(String(256))
    Longtitude = Column(Float)
    latitude = Column(Float)
    owner_id = Column(String(60), ForeignKey("users.id"), nullable=True)
    hub_id = Column(String(60), ForeignKey("hubs.id"), nullable=True)

    def __init__(self, *args, **kwargs):
        """initializes Location class"""
        super().__init__(*args, **kwargs)
