import unittest
import unittest.mock
import api.routers.oauth2_client as oauth2_client

class Oauth2ClientTest(unittest.TestCase):

    def testThrowsForRequiredEnvVars(self):
        self.assertEquals(True, False)
    

    def testHasTheJohnDeereCallbackRoute(self):
        self.assertEquals(True, False)

    # TODO: automocking OAuth2Session & asserting about constructors?
    # TODO: "in place spy" / monkey patch to make observations on calls on `jd_oauth2_session`
    # TODO: SessionMiddleware testing 
    # TODO: auto hydrate starlette Request
    # TODO: automocking requests.Response (was done successfully in  test_ecs but in this example more dependencies on output/makeup of the automock )