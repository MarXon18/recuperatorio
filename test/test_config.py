import os
from flask import Flask
import unittest
from app.config import config

class TestConfig(unittest.TestCase):
    def test_config_factory(self):
        app_context = 'development'
        expected_config = config.DevelopmentConfig
        self.assertEqual(config.factory(app_context), expected_config)

        app_context = 'production'
        expected_config = config.ProductionConfig
        self.assertEqual(config.factory(app_context), expected_config)

        app_context = 'testing'
        expected_config = config.TestConfig
        self.assertEqual(config.factory(app_context), expected_config)

    def test_config_attributes(self):
        app_context = 'development'
        config_obj = config.factory(app_context)

        self.assertTrue(config_obj.DEBUG)
        self.assertTrue(config_obj.SQLALCHEMY_TRACK_MODIFICATIONS)
        self.assertEqual(config_obj.SQLALCHEMY_DATABASE_URI, os.environ.get('DEV_DATABASE_URI'))

        app_context = 'production'
        config_obj = config.factory(app_context)

        self.assertFalse(config_obj.DEBUG)
        self.assertFalse(config_obj.SQLALCHEMY_TRACK_MODIFICATIONS)
        self.assertEqual(config_obj.SQLALCHEMY_DATABASE_URI, os.environ.get('PROD_DATABASE_URI'))

    def test_config_init_app(self):
        app_context = 'development'
        config_obj = config.factory(app_context)
        app = Flask(__name__)
        config_obj.init_app(app)

        self.assertEqual(app.config['DEBUG'], config_obj.DEBUG)
        self.assertEqual(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'], config_obj.SQLALCHEMY_TRACK_MODIFICATIONS)
        self.assertEqual(app.config['SQLALCHEMY_DATABASE_URI'], config_obj.SQLALCHEMY_DATABASE_URI)

if __name__ == '__main__':
    unittest.main()