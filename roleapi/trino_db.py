import trino

class Trino:
    def __init__(self):
        self.app = None
        self.driver = None

    def init_app(self, app):
        self.app = app
        self.connect()

    def connect(self):
        self.driver = trino.dbapi.connect(
            host = self.app.config['TRINO_HOST'],
            port = self.app.config['TRINO_PORT'],
            http_scheme = 'https',
            catalog = self.app.config['TRINO_CATALOG'],
            schema = self.app.config['TRINO_SCHEMA'],
            auth = trino.auth.BasicAuthentication(self.app.config['TRINO_USER'], self.app.config['TRINO_PASSWORD'])
        )
        return self.driver

    def get_db(self):
        if not self.driver:
            return self.connect()
        return self.driver