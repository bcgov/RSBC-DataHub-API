import os
from unittest import TestCase
import json



# To override the config class for testing
class Config(ValidationConfig):
    SCHEMA_FILENAME         = 'validator/schemas.json'
    

class TestIngestor(TestCase):

    def setUp(self):
        self.app = create_app('development')
        self.client = self.app.test_client()
        db.create_all(app=self.app)

    def tearDown(self):
        db.session.remove()
        db.drop_all(app=self.app)

    def test_create_company(self):
        data = dict(name='test', country_code='IE', website='http://example.com', enabled=True)
        response = self.client.post('/companies', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 200

