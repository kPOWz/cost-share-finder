
import unittest
import unittest.mock
import api.ecs as ECS

class ElasticContainerServiceTest(unittest.TestCase):

    @unittest.mock.patch('os.getenv')
    @unittest.mock.patch('requests.get')
    def testGetsMetaDataEnvironmentVariable(self, requests_get, os_getenv):
        ecs_metadata_autoinjected_environment_var = "ECS_CONTAINER_METADATA_URI_V4"
        ecs_metadata_url = 'https://www.aws_base_url.fake'

        os_getenv.return_value = ecs_metadata_url

        ECS.get_task_metadata('http:anything')

        os_getenv.assert_called_once_with(ecs_metadata_autoinjected_environment_var)
 
    @unittest.mock.patch('os.getenv') # mock the whole module instead?
    @unittest.mock.patch('requests.get')
    def testUsesMetaDataEnvironmentVariableForTask(self, requests_get, os_getenv):
        ecs_metadata_url = 'https://www.aws_base_url.fake'
        ecs_task_metadata_url = "{}/task".format(ecs_metadata_url)

        os_getenv.return_value = ecs_metadata_url

        ECS.get_task_metadata('http:anything')

        # should this be called async instead?
        requests_get.assert_called_once_with(ecs_task_metadata_url)
    
    @unittest.mock.patch('os.getenv') # mock the whole module instead?
    @unittest.mock.patch('requests.get')
    def testUsesDefaultWhenMetaDataEnvironmentVariableForTaskUnavailable(self, requests_get, os_getenv):
        request_url = 'http://anything'
        ecs_task_metadata_url = "{}/static/missing_env.json".format(request_url)

        os_getenv.return_value = None

        ECS.get_task_metadata(request_url)

        requests_get.assert_called_once_with(ecs_task_metadata_url)
    
    @unittest.mock.patch('os.getenv') # mock the whole module instead?
    @unittest.mock.patch('requests.get')
    @unittest.mock.patch('requests.Response', autospec=True)
    def testReturnsJsonMetadata(self, requests_Response_automock, requests_get, os_getenv):
        ecs_metadata_url = 'https://www.aws_base_url.fake'
        expected_json = {
            "Family": "la",
            "Revision": "3",
            "DesiredStatus": "RUNNING",
            "KnownStatus": "RUNNING"
        }

        os_getenv.return_value = ecs_metadata_url
        requests_get.return_value = requests_Response_automock
        requests_Response_automock.json.return_value = expected_json

        observed = ECS.get_task_metadata('http:anything')

        requests_Response_automock.json.assert_called_once()
        self.assertEquals(expected_json, observed)


    @unittest.mock.patch('os.getenv') # mock the whole module instead?
    @unittest.mock.patch('requests.get')
    @unittest.mock.patch('requests.Response', autospec=True)
    def testCallsRaisesBeforeAssumingHappyJson(self, requests_Response_automock, requests_get, os_getenv):
        ecs_metadata_url = 'https://www.aws_base_url.fake'

        os_getenv.return_value = ecs_metadata_url
        requests_get.return_value = requests_Response_automock

        ECS.get_task_metadata('http:anything')

        requests_Response_automock.raise_for_status.assert_called_once()