import requests
from app import app


class TesterClass(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def setUp(self):
        response = requests.get('http://127.0.0.1:5000')
        self.asserE




