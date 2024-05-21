#!/usr/bin/python3
"""
model to manage DB storage using sqlAlchemy
"""
from models.base_model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.categories import Category
from models.hubs import Hub
from models.users import User
from models.products import Product
from models.sales import Purchase, SoldProduct
from models.reviews import Review
from models.images import Image
from models.locations import Location
from os import getenv


class DBStorage:
    """
        This class manage DB storage for Haverst
        Harbor using sqlAlchemy
    """
    __engine = None
    __session = None
    all_classes = {
        "User": User,
        "Location": Location,
        "Category": Category,
        "Hub": Hub,
        "Image": Image,
        "product": Product,
        "Sale": Purchase,
        "Review": Review,
        "SoldProduct": SoldProduct,
        }

    def __init__(self):
        """
            Init __engine based on the Enviroment
        """
        HH_MYSQL_USER = getenv('HH_MYSQL_USER')
        HH_MYSQL_PWD = getenv('HH_MYSQL_PWD')
        HH_MYSQL_HOST = getenv('HH_MYSQL_HOST')
        HH_MYSQL_DB = getenv('HH_MYSQL_DB')
        HH_ENV = getenv('HH_ENV')
        exec_db = 'mysql+mysqldb://{}:{}@{}/{}'.format(
                                            HH_MYSQL_USER,
                                            HH_MYSQL_PWD,
                                            HH_MYSQL_HOST,
                                            HH_MYSQL_DB
                                                )
        self.__engine = create_engine(exec_db, pool_pre_ping=True)
        if HH_ENV == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ query on the current database session (self.__session)
        all objects depending of the class name"""
        result = []
        if cls:
            q = self.__session.query(cls).all()
            return (q)
        else:
            for key in self.all_classes.keys():
                c = self.all_classes
                q = self.__session.query(c[key]).all()
                result.append(q)
            return (result)

    def new(self, obj):
        """
            Creating new instance in db storage
        """
        self.__session.add(obj)

    def save(self):
        """
            save to the db storage
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
            Delete obj from db storage
        """
        if obj:
            self.__session.delete(obj)
        self.save()

    def reload(self):
        """
            create table in database
        """
        Base.metadata.create_all(self.__engine)
        session_db = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_db)
        self.__session = Session()

    def close(self) -> None:
        """
            Closing the session
        """
        self.reload()
        self.__session.close()

    @staticmethod
    def to_dict(query) -> dict:
        """method to turn a query object into a class
        Arg:
            query: The query object
        Return: A dictionary of query contents
        """
        final = {}
        for instance in query:
            instance_key = instance.__class__.__name__ + '.' + instance.id
            final[instance_key] = instance
        return (final)

    def get(self, cls, id=None, token=None, **kwargs) -> object:
        """retrieve one object based on cls and id
        Args:
            cls: class of the object
            id: Id of the object
        Return: object based on the class and its ID, or None
        """
        if id:
            q = self.__session.query(cls).filter_by(id=id).one_or_none()
        elif cls.__name__ == "User":
            # query by email or phone_number (works for user table)
            if 'email' in kwargs.keys():
                email = kwargs.get('email')
                q = self.__session.query(cls).\
                    filter_by(email=email).one_or_none()
            elif 'phone_number' in kwargs.keys():
                number = kwargs.get('phone_number')
                q = self.__session.query(cls).\
                    filter_by(phone_number=number).one_or_none()
        elif token and cls.__name__ == "BlacklistToken":
            q = self.__session.query(cls).filter_by(token=token).one_or_none()
        elif "name" in kwargs.keys() and hasattr(cls, "name"):
            q = self.__session.query(cls).filter_by(name=kwargs["name"]).all()
        if q:
            return (q)

    def count(self, cls=None) -> int:
        """count the number of objects in storage:
        Args:
            cls: class of the objects
        Return: number of objects in storage matching the given class
                if no class is passed,
                returns the count of all objects in storage.
        """
        if cls:
            return (len(self.all(cls)))
        return (len(self.all()))
