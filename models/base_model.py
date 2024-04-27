#!/usr/bin/python3
"""Base Model - Module
Description:
    It holds common (a union of) characteristics for other models
    Its herited by other model classes in this project
"""
import models
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Column, DateTime
from os import getenv


Base = declarative_base()


class BaseModel:
    """Holds common model attrs and functions for this project
    Attrs:
        id: ID of the row in the database
        created_at: the time the row was created
        updated_at: When the row was last edited
    """
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime(), default=datetime.now(), nullable=False)
    updated_at = Column(DateTime(), default=datetime.now(), nullable=False)

    def __init__(self, *args, **kwargs) -> None:
        """Intializes the class
        Args:
            args: unused arguments
            kwargs: a dictionary of elements used to create
                    object attributes names (only if kwargs is not empty)
        Return: None
        """
        if kwargs:
            int_attrs = [
                "quantities",
            ]
            float_attrs = [
                "unit_price",
                "longtitude",
                "latitude"
            ]
            obj_id = getattr(kwargs, "id", None)
            if obj_id is None:
                self.id = str(uuid4())
                self.created_at = datetime.now()
                self.updated_at = datetime.now()
            for key in kwargs.keys():
                if key == "created_at":
                    self.created_at = datetime\
                        .fromisoformat(kwargs[key])
                elif key == "updated_at":
                    self.updated_at = datetime\
                        .fromisoformat(kwargs[key])
                elif key == "id":
                    self.id = kwargs[key]
                elif key in int_attrs:
                    setattr(self, key, int(kwargs[key]))
                elif key in float_attrs:
                    setattr(self, key, float(kwargs[key]))
                else:
                    setattr(self, key, kwargs[key])
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def save(self) -> None:
        """
        Description:
            Update the updated_at field with current date
            and save to JSON file
        """
        # If storage is database, Update the date if the object dict
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def delete(self) -> None:
        """delete the current instance from the storage"""
        models.storage.delete(self)

    def __str__(self) -> str:
        """Return string representation of the object"""
        self_dict = self.__dict__
        if "_sa_instance_state" in self_dict:
            del self_dict['_sa_instance_state']
        rep = "[{}] ({}) {}".format(self.__class__.__name__,
                                    self.id, self_dict)
        return (rep)
