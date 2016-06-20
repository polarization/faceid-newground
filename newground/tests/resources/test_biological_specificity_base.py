# coding=utf-8
from newground.tests.base import ResourcesTestCase
import os
import json
import redis


class biological_specificity_base_TestCase(ResourcesTestCase):

    def setUp(self):
        super(biological_specificity_base_TestCase, self).setUp()
        with open('test_upload.txt', 'wb') as upload_file:
            upload_file.write('Hello world!')

        pool = redis.ConnectionPool(host='10.101.2.9', port=6379, db=0)
        redis_cli = redis.Redis(connection_pool=pool)

        redis_cli.set('FDBInfo',
                      '{"fdb1":"beijingbranch",'
                      '"fdb2":"shanghaibranch",'
                      '"fdb3":"test:tester"}')
        redis_cli.set('SwiftAccountInfo',
                      '{"beijingbranch":"key1", '
                      '"shanghaibranch":"key2", '
                      '"test:tester":"testing"}')

    def tearDown(self):
        super(biological_specificity_base_TestCase, self).tearDown()
        if os.path.isfile('test_upload.txt'):
            os.remove('test_upload.txt')

    def test_livesample_create(self):
        response = self.web_client.post('/livesample/create',
                                        {'fdbname': 'fdb3'},
                                        upload_files=[('samplefile',
                                                       'test_upload.txt')])
        self.assertEqual(200, response.status_code)
        self.assertEqual('application/json', response.content_type)
        self.assertEqual('success', json.loads(response.body)['result'])

    def test_fdbname_update(self):
        response = self.web_client.post('/fdb/fdb3/update',
                                        {'newfdbname': 'fdb5'})
        self.assertEqual(200, response.status_code)
        self.assertEqual('application/json', response.content_type)
        self.assertEqual({"result": "success"}, json.loads(response.body))

        response = self.web_client.post('/fdb/fdb5/update',
                                        {'newfdbname': 'fdb3'})
        self.assertEqual(200, response.status_code)
        self.assertEqual('application/json', response.content_type)
        self.assertEqual({"result": "success"}, json.loads(response.body))

        response = self.web_client.post('/fdb/fdb4/update',
                                        {'newfdbname': 'fdb5'})
        self.assertEqual(200, response.status_code)
        self.assertEqual('application/json', response.content_type)
        self.assertEqual({"result": "fail", 'error': 'fdb not exists'},
                         json.loads(response.body))
