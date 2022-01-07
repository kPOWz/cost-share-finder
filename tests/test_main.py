from fastapi.testclient import TestClient
import unittest
import unittest.mock

from api.main import app

client = TestClient(app)

class Oauth2ClientTest(unittest.TestCase):

    @unittest.mock.patch('api.ecs.get_task_metadata')
    def test_has_healthcheck_route(self, get_task_metadata):
        response = client.get("/")

        self.assertEquals(200, response.status_code)
    
    @unittest.mock.patch('api.ecs.get_task_metadata')
    def test_healthcheck_returns_ecs_metadata(self, get_task_metadata):
        get_task_metadata.return_value = {"some": "json"}

        response = client.get("/")

        get_task_metadata.assert_called_once()
        self.assertEquals({"some": "json"}, response.json())