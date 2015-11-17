import logging.config
import re
import os
from unittest import TestCase
from mock import patch


class RegexpMatch(str):
    def __eq__(self, other):
        return re.match(self, other) != None


class TestConfigFileLogging(TestCase):

    def test_simple_config(self):
        with patch('logging.codecs') as codecs_mock:
            config_file = os.path.join(os.path.dirname(__file__), "config_file.conf")
            logging.config.fileConfig(config_file, disable_existing_loggers=True)
            test_logger = logging.getLogger("test")

        test_logger.info("Msg")
        codecs_mock.open.assert_called_once_with('/test/fake_file.log', 'a', 'UTF-8')
        codecs_mock.open.return_value.write.assert_called_once_with(RegexpMatch(
            '{"time": "[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}Z", '
            '"lvl": "INFO", "corr": null, "trans": null, "op": null, '
            '"comp": "tests_config_file", "msg": "Msg"}\n'))
