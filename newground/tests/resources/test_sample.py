from newground.tests.base import ResourcesTestCase


class SampleTestCase(ResourcesTestCase):

    def test_log(self):
        response = self.web_client.get('/logs/1')
        self.assertEqual(200, response.status_code)
        self.assertEqual('application/json', response.content_type)
        self.assertEqual('{\n  "result": true\n}', response.body)
