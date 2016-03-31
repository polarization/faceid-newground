# -*- coding: UTF-8 -*-
import fixtures
import os
import testtools
import test_config

from newground import app
from flask.ext.webtest import TestApp


class Config(fixtures.Fixture):

    def __init__(self, conf=test_config):
        self.conf = conf

    def setUp(self):
        super(Config, self).setUp()
        self.addCleanup(self._reset_default_config_files)

    def config(self, **kw):
        for k, v in kw:
            self.conf.k = v

    def _reset_default_config_files(self):
        self.conf = test_config

    def set_config_files(self, config_file):
        self.conf = config_file


class TestCase(testtools.TestCase):

    def setUp(self):
        super(TestCase, self).setUp()
        test_timeout = os.environ.get('OS_TEST_TIMEOUT', 0)
        try:
            test_timeout = int(test_timeout)
        except ValueError:
            test_timeout = 0
        if test_timeout > 0:
            self.useFixture(fixtures.Timeout(test_timeout, gentle=True))
        self.useFixture(fixtures.NestedTempfile())
        self.useFixture(fixtures.TempHomeDir())
        self.log_fixture = self.useFixture(fixtures.FakeLogger())
        self._set_config()
        self.addCleanup(self._clear_attrs)

    def _set_config(self):
        self.cfg_fixture = self.useFixture(Config())
        self.config()

    def _clear_attrs(self):
        for key in [k for k in self.__dict__.keys() if k[0] != '_']:
            del self.__dict__[key]

    def config(self, **kw):
        self.cfg_fixture.config(**kw)


class ResourcesTestCase(TestCase):

    def setUp(self):
        super(ResourcesTestCase, self).setUp()
        self.app = app.create_app()
        self.web_client = TestApp(self.app)
