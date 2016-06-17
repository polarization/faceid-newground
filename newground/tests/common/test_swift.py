# coding=utf-8
from newground.tests.base import TestCase
from newground.common import swift
import os


class SampleTestCase(TestCase):

    def setUp(self):
        super(SampleTestCase, self).setUp()
        with open('hello.txt', 'w') as file:
            file.write('hello world')

    def tearDown(self):
        super(SampleTestCase, self).tearDown()
        os.remove('hello.txt')
        # os.remove('hello1.txt')

    def test_swift_api(self):
        pass
        #self.assertEqual(True, swift.create_container('leixun'))
        # self.assertEqual(True, swift.create_object('hello.txt', 'leixun',
        #                                            'hello.txt',
        #                                            'text/plain'))
        # self.assertEqual(True, 'leixun' in swift.get_container_names())
        # self.assertEqual(True, 'hello.txt' in swift.get_file_list('leixun'))
        #
        # swift.get_object('leixun', 'hello.txt', 'hello1.txt')
        # # self.assertEqual(True, 'hello.txt' in swift.get_object('leixun',
        # # 'hello.txt', 'hello1.txt'))
        #
        # self.assertEqual(True, swift.delete_object('leixun', 'hello.txt'))
        # self.assertEqual(True, swift.delete_container('leixun'))
