#!/usr/bin/python3
"""Test Database storage module"""
import unittest
import pycodestyle
import inspect
from models import storage, Location, Category, User, Hub, db_storage
from os import getenv


if getenv('HH_MYSQL_DB') == 'test':
    class Test_database_storage(unittest.TestCase):
        """
        Test class for Database storage
        All test cases writen in method like tests
        """

        @classmethod
        def setUpClass(cls) -> None:
            """Setup model instance to use in the test cases"""
            cls.fun_names = [name for name, _ in
                                inspect.getmembers(db_storage.DBStorage,
                                                inspect.ismethod)]
            cls.user = User(email="jk@gmail.com", password="@123nn",
                            phone_number="+256705688714", username='Kenneth')
            cls.user1 = User(email="tayebwaian@gmail.com", username="Mark",
                             phone_number="+256785698716", password="@123nn")
            cls.user2 = User(email="dym@yahoo.com", username="Denash",
                             phone_number="+25675608736", password="@123nn")
            cls.category = Category(name="fruits")
            cls.location = Location(country="Uganda", owner_id=cls.user.id,
                                    district='kabale', state='kigezi')
            cls.hub = Hub(name="Fresh Fruit Shop",
                           description='One stop stand for fresh garden fruits',
                           owner_id=cls.user1, status='active')

        def test_return_value_of_all_function(self) -> None:
            """Test the return value of all function"""
            self.user.save()
            self.category.save()
            self.hub.save()
            self.location.save()
            data = storage.all()
            key = self.user1.__class__.__name__ + ".{}".format(self.user.id)
            data[key] = self.user1
            self.user1.save()
            updated_data = storage.all()
            self.assertEqual(data, updated_data, "Not all objects in \
                                database is returned")

        def test_database_update(self) -> None:
            """Check if the Database is updated with new obj
            Upon creation of a new obj
            """
            data = storage.all()
            self.user.save()
            self.assertEqual(len(data) + 1, len(storage.all()))

        def test_documentation(self) -> None:
            """Test if module, class and methods documentations exist"""
            self.assertGreater(len(storage.__doc__), 0)
            self.assertGreater(len(db_storage.__doc__), 0)
            for func in self.fun_names:
                with self.subTest(func):
                    self.assertGreater(len(func.__doc__), 0,
                                        "Missing documentation \
                                        of {} method".format(func))

        def test_pep8_complaince(self) -> None:
            """Check if module is complaint when you run pycodestyle on it"""
            style_checker = pycodestyle.StyleGuide()
            result = style_checker.check_files(['models/\
                                                engine/db_storage.py'])
            self.assertEqual(result.total_errors, 0, "PEP 8 violations found")

        def test_get_function(self) -> None:
            """test retrieving of a single object"""
            obj = self.user2
            obj.save()
            result = storage.get(User, self.user2.id)
            self.assertEqual(obj.id, result.id,
                                "A single object can not be retrieved")

        def test_count_function(self) -> None:
            """
            Check if the correct number of all object in storage is returned
            """
            for key in storage.all().keys():
                storage.all()[key].delete()
            self.user.save()
            self.category.save()
            self.hub.save()
            self.location.save()
            self.user1.save()
            self.assertEqual(5, len(storage.all()),
                                "Incorrect count for the number \
                                of objects in file storage")

    if __name__ == "__main__":
        unittest.main()
