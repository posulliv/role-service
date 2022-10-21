import os

class ProdConfig:
    TRINO_PORT = os.environ.get('TRINO_PORT')
    TRINO_HOST = os.environ.get('TRINO_HOST')
    TRINO_CATALOG = os.environ.get('TRINO_CATALOG')
    TRINO_SCHEMA = os.environ.get('TRINO_SCHEMA')
    TRINO_USER = os.environ.get('TRINO_USER')
    TRINO_PASSWORD = os.environ.get('TRINO_PASSWORD')


class DevConfig:
    TRINO_PORT = os.environ.get('TRINO_PORT')
    TRINO_HOST = os.environ.get('TRINO_HOST')
    TRINO_CATALOG = os.environ.get('TRINO_CATALOG')
    TRINO_SCHEMA = os.environ.get('TRINO_SCHEMA')
    TRINO_USER = os.environ.get('TRINO_USER')
    TRINO_PASSWORD = os.environ.get('TRINO_PASSWORD')

class TestConfig:
    TRINO_PORT = os.environ.get('TRINO_PORT')
    TRINO_HOST = os.environ.get('TRINO_HOST')
    TRINO_CATALOG = os.environ.get('TRINO_CATALOG')
    TRINO_SCHEMA = os.environ.get('TRINO_SCHEMA')
    TRINO_USER = os.environ.get('TRINO_USER')
    TRINO_PASSWORD = os.environ.get('TRINO_PASSWORD')

config = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig
}
