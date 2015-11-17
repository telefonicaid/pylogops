import logging
import re
import time
from unittest import TestCase
from mock import patch, call
from pylogops.logger import TrackingFilter, JsonFormatter
from logging import FileHandler
from pylogops import local_context


class RegexpMatch(str):
    def __eq__(self, other):
        return re.match(self, other) != None


class TestBasicConfigLogging(TestCase):

    def test_json_formater(self):
        with patch('logging.codecs') as codecs_mock:
            file_handler = FileHandler('/test/fake_file.log', encoding='UTF-8')
            file_handler.addFilter(TrackingFilter())
            file_handler.setFormatter(JsonFormatter())
            logging.basicConfig()
            test_logger = logging.getLogger("test")
            test_logger.addHandler(file_handler)
            test_logger.setLevel(logging.DEBUG)

        test_logger.info("Msg")
        codecs_mock.open.assert_called_once_with('/test/fake_file.log', 'a', 'UTF-8')
        codecs_mock.open.return_value.write.assert_called_once_with(RegexpMatch(
            '{"time": "[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}Z", '
            '"lvl": "INFO", "corr": null, "trans": null, "op": null, '
            '"comp": "tests_basic_config", "msg": "Msg"}\n'))

    def test_json_formater_with_localtime(self):
        with patch('logging.codecs') as codecs_mock:
            file_handler = FileHandler('/test/fake_file.log', encoding='UTF-8')
            file_handler.addFilter(TrackingFilter())
            file_handler.setFormatter(JsonFormatter(converter=time.localtime))
            logging.basicConfig()
            test_logger = logging.getLogger("test")
            test_logger.addHandler(file_handler)
            test_logger.setLevel(logging.DEBUG)

        test_logger.info("Msg")
        codecs_mock.open.assert_called_once_with('/test/fake_file.log', 'a', 'UTF-8')
        codecs_mock.open.return_value.write.assert_called_once_with(RegexpMatch(
            '{"time": "[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}Z", '
            '"lvl": "INFO", "corr": null, "trans": null, "op": null, '
            '"comp": "tests_basic_config", "msg": "Msg"}\n'))

    def test_json_formater_with_keys_fmt(self):
        with patch('logging.codecs') as codecs_mock:
            file_handler = FileHandler('/test/fake_file.log', encoding='UTF-8')
            file_handler.addFilter(TrackingFilter())
            file_handler.setFormatter(JsonFormatter(keys_fmt=[('lvl', 'levelname'), ('msg', 'message')]))
            logging.basicConfig()
            test_logger = logging.getLogger("test")
            test_logger.addHandler(file_handler)
            test_logger.setLevel(logging.DEBUG)

        test_logger.info("Msg")
        codecs_mock.open.assert_called_once_with('/test/fake_file.log', 'a', 'UTF-8')
        codecs_mock.open.return_value.write.assert_called_once_with(RegexpMatch(
            '{"lvl": "INFO", "msg": "Msg"}\n'))

    def test_json_formater_removing_empty_keys(self):
        with patch('logging.codecs') as codecs_mock:
            file_handler = FileHandler('/test/fake_file.log', encoding='UTF-8')
            file_handler.addFilter(TrackingFilter())
            file_handler.setFormatter(JsonFormatter(remove_blanks=True))
            logging.basicConfig()
            test_logger = logging.getLogger("test")
            test_logger.addHandler(file_handler)
            test_logger.setLevel(logging.DEBUG)

        test_logger.info("Msg")
        codecs_mock.open.assert_called_once_with('/test/fake_file.log', 'a', 'UTF-8')
        codecs_mock.open.return_value.write.assert_called_once_with(RegexpMatch(
            '{"time": "[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}Z", '
            '"lvl": "INFO", "comp": "tests_basic_config", "msg": "Msg"}\n'))

    def test_json_formater_with_extra(self):
        with patch('logging.codecs') as codecs_mock:
            file_handler = FileHandler('/test/fake_file.log', encoding='UTF-8')
            file_handler.addFilter(TrackingFilter())
            file_handler.setFormatter(JsonFormatter())
            logging.basicConfig()
            test_logger = logging.getLogger("test")
            test_logger.addHandler(file_handler)
            test_logger.setLevel(logging.DEBUG)

        test_logger.info("Msg", extra={'additional': {'key': 'extra'}})
        codecs_mock.open.assert_called_once_with('/test/fake_file.log', 'a', 'UTF-8')
        codecs_mock.open.return_value.write.assert_called_once_with(RegexpMatch(
            '{"time": "[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}Z", '
            '"lvl": "INFO", "corr": null, "trans": null, "op": null, '
            '"comp": "tests_basic_config", "msg": "Msg", "key": "extra"}\n'))

    def test_json_formater_with_transaction(self):
        with patch('logging.codecs') as codecs_mock:
            file_handler = FileHandler('/test/fake_file.log', encoding='UTF-8')
            file_handler.addFilter(TrackingFilter())
            file_handler.setFormatter(JsonFormatter())
            logging.basicConfig()
            test_logger = logging.getLogger("test")
            test_logger.addHandler(file_handler)
            test_logger.setLevel(logging.DEBUG)
            local_context.transaction_id = "trans"
            local_context.correlator_id = "corr"
            local_context.op_type = "op"
            test_logger.info("Msg1")
            test_logger.debug("Msg2")
            test_logger.error("Msg3")
            codecs_mock.open.assert_called_once_with('/test/fake_file.log', 'a', 'UTF-8')
            codecs_mock.open.return_value.write.assert_has_calls([
                call(RegexpMatch('{"time": "[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}Z", '
                                 '"lvl": "INFO", "corr": "corr", "trans": "trans", "op": "op", '
                                 '"comp": "tests_basic_config", "msg": "Msg1"}\n')),
                call(RegexpMatch('{"time": "[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}Z", '
                                 '"lvl": "DEBUG", "corr": "corr", "trans": "trans", "op": "op", '
                                 '"comp": "tests_basic_config", "msg": "Msg2"}\n')),
                call(RegexpMatch('{"time": "[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}Z", '
                                 '"lvl": "ERROR", "corr": "corr", "trans": "trans", "op": "op", '
                                 '"comp": "tests_basic_config", "msg": "Msg3"}\n'))
            ])
