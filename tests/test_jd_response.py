import unittest
from api.models.jd_response import JDResponse

class JDResponseTest(unittest.TestCase):

    def testModelIgnoresExtra(self):
        expected_json = {
            "bunny": "rabbit",
            "@type": "ApiCatalog",
            "links": [{"@type":"Link","rel":"currentUser","uri":"https://sandboxapi.deere.com/platform/users/@currentUser"},
                        {"@type":"Link","rel":"organizations","uri":"https://sandboxapi.deere.com/platform/organizations"}]
        }

        resp = JDResponse.parse_obj(expected_json)

        self.assertEquals(2, len(resp.links))