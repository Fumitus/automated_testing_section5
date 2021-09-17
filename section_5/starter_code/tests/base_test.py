"""
BaseTest

This class should be parent class for non-unit tests.
It allows instantiations of the database dynamically and makes sure
that it is new, blank database each time.
"""

from unittest import TestCase
from section_5.starter_code.app import app
from ..db import db


class BaseTest(TestCase):
    def setUp(self) -> None:
        # Make sure database exists
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        with app.app_context():
            db.init_app(app)
            db.create_all()
        # Get test client
        self.app = app.test_client()
        self.app_context = app.app_context

    def tearDown(self) -> None:
        # Database is blank
        with app.app_context():
            db.session.remove()
            db.drop_all()
