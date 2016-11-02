import logging.config
import re
import os
import six
from unittest import TestCase
if six.PY3:
    from unittest.mock import patch, call  # @UnusedImport @UnresolvedImport
else:
    from mock import patch, call  # @Reimport @UnresolvedImport


class RegexpMatch(object):

    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return re.match(self.value, other) != None


class TestConfigFileLogging(TestCase):

    def setUp(self):
        if six.PY3:
            self.patch_open = patch('builtins.open')
        else:
            self.patch_open = patch('logging.codecs.open')
        TestCase.setUp(self)

    def test_simple_config(self):
        config_file = open(os.path.join(os.path.dirname(__file__), "config_file.conf"))
        with self.patch_open as open_mock:
            logging.config.fileConfig(config_file, disable_existing_loggers=True)
            test_logger = logging.getLogger("test")

        test_logger.info("Msg")
        if six.PY3:
            open_mock.assert_called_once_with('/test/fake_file.log', 'a', encoding='UTF-8')
            open_mock.return_value.write.assert_has_calls([call(RegexpMatch(
                '{"time":"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}Z",'
                '"lvl":"INFO","corr":null,"trans":null,"op":null,'
                '"comp":"tests_config_file","msg":"Msg"}')), call('\n')])
        else:
            open_mock.assert_called_once_with('/test/fake_file.log', 'a', 'UTF-8')
            open_mock.return_value.write.assert_called_once_with(RegexpMatch(
                '{"time":"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}Z",'
                '"lvl":"INFO","corr":null,"trans":null,"op":null,'
                '"comp":"tests_config_file","msg":"Msg"}\n'))
