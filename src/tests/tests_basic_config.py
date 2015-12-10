import logging
import re
import time
import six
from unittest import TestCase
from pylogops.logger import TrackingFilter, JsonFormatter
from logging import FileHandler
from pylogops import local_context
if six.PY3:
    from unittest.mock import patch, call  # @UnusedImport @UnresolvedImport
else:
    from mock import patch, call  # @Reimport @UnresolvedImport


class RegexpMatch(object):

    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return re.match(self.value, other) != None


class TestBasicConfigLogging(TestCase):

    def setUp(self):
        if six.PY3:
            self.patch_open = patch('builtins.open')
        else:
            self.patch_open = patch('logging.codecs.open')
        TestCase.setUp(self)

    def test_json_formater(self):
        with self.patch_open as open_mock:
            file_handler = FileHandler('/test/fake_file.log', encoding='UTF-8')
            file_handler.addFilter(TrackingFilter())
            file_handler.setFormatter(JsonFormatter())
            logging.basicConfig()
            test_logger = logging.getLogger("test")
            test_logger.addHandler(file_handler)
            test_logger.setLevel(logging.DEBUG)

        test_logger.info("Msg")
        if six.PY3:
            open_mock.assert_called_once_with('/test/fake_file.log', 'a', encoding='UTF-8')
            open_mock.return_value.write.assert_has_calls([call(RegexpMatch(
                '{"time": "[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}Z", '
                '"lvl": "INFO", "corr": null, "trans": null, "op": null, '
                '"comp": "tests_basic_config", "msg": "Msg"}')), call('\n')])
        else:
            open_mock.assert_called_once_with('/test/fake_file.log', 'a', 'UTF-8')
            open_mock.return_value.write.assert_called_once_with(RegexpMatch(
                '{"time": "[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}Z", '
                '"lvl": "INFO", "corr": null, "trans": null, "op": null, '
                '"comp": "tests_basic_config", "msg": "Msg"}\n'))

    def test_json_formater_with_localtime(self):
        with self.patch_open as open_mock:
            file_handler = FileHandler('/test/fake_file.log', encoding='UTF-8')
            file_handler.addFilter(TrackingFilter())
            file_handler.setFormatter(JsonFormatter(converter=time.localtime))
            logging.basicConfig()
            test_logger = logging.getLogger("test")
            test_logger.addHandler(file_handler)
            test_logger.setLevel(logging.DEBUG)

        test_logger.info("Msg")
        if six.PY3:
            open_mock.assert_called_once_with('/test/fake_file.log', 'a', encoding='UTF-8')
            open_mock.return_value.write.assert_has_calls([call(RegexpMatch(
                '{"time": "[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}Z", '
                '"lvl": "INFO", "corr": null, "trans": null, "op": null, '
                '"comp": "tests_basic_config", "msg": "Msg"}')), call('\n')])
        else:
            open_mock.assert_called_once_with('/test/fake_file.log', 'a', 'UTF-8')
            open_mock.return_value.write.assert_called_once_with(RegexpMatch(
                '{"time": "[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}Z", '
                '"lvl": "INFO", "corr": null, "trans": null, "op": null, '
                '"comp": "tests_basic_config", "msg": "Msg"}\n'))

    def test_json_formater_with_keys_fmt(self):
        with self.patch_open as open_mock:
            file_handler = FileHandler('/test/fake_file.log', encoding='UTF-8')
            file_handler.addFilter(TrackingFilter())
            file_handler.setFormatter(JsonFormatter(keys_fmt=[('lvl', 'levelname'), ('msg', 'message')]))
            logging.basicConfig()
            test_logger = logging.getLogger("test")
            test_logger.addHandler(file_handler)
            test_logger.setLevel(logging.DEBUG)

        test_logger.info("Msg")
        if six.PY3:
            open_mock.assert_called_once_with('/test/fake_file.log', 'a', encoding='UTF-8')
            open_mock.return_value.write.assert_has_calls([call(RegexpMatch(
                '{"lvl": "INFO", "msg": "Msg"}')), call('\n')])
        else:
            open_mock.assert_called_once_with('/test/fake_file.log', 'a', 'UTF-8')
            open_mock.return_value.write.assert_called_once_with(RegexpMatch(
                '{"lvl": "INFO", "msg": "Msg"}\n'))

    def test_json_formater_removing_empty_keys(self):
        with self.patch_open as open_mock:
            file_handler = FileHandler('/test/fake_file.log', encoding='UTF-8')
            file_handler.addFilter(TrackingFilter())
            file_handler.setFormatter(JsonFormatter(remove_blanks=True))
            logging.basicConfig()
            test_logger = logging.getLogger("test")
            test_logger.addHandler(file_handler)
            test_logger.setLevel(logging.DEBUG)

        test_logger.info("Msg")
        if six.PY3:
            open_mock.assert_called_once_with('/test/fake_file.log', 'a', encoding='UTF-8')
            open_mock.return_value.write.assert_has_calls([call(RegexpMatch(
                '{"time": "[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}Z", '
                '"lvl": "INFO", "comp": "tests_basic_config", "msg": "Msg"}')), call('\n')])
        else:
            open_mock.assert_called_once_with('/test/fake_file.log', 'a', 'UTF-8')
            open_mock.return_value.write.assert_called_once_with(RegexpMatch(
                '{"time": "[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}Z", '
                '"lvl": "INFO", "comp": "tests_basic_config", "msg": "Msg"}\n'))

    def test_json_formater_with_extra(self):
        with self.patch_open as open_mock:
            file_handler = FileHandler('/test/fake_file.log', encoding='UTF-8')
            file_handler.addFilter(TrackingFilter())
            file_handler.setFormatter(JsonFormatter())
            logging.basicConfig()
            test_logger = logging.getLogger("test")
            test_logger.addHandler(file_handler)
            test_logger.setLevel(logging.DEBUG)

        test_logger.info("Msg", extra={'additional': {'key': 'extra'}})
        if six.PY3:
            open_mock.assert_called_once_with('/test/fake_file.log', 'a', encoding='UTF-8')
            open_mock.return_value.write.assert_has_calls([call(RegexpMatch(
                '{"time": "[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}Z", '
                '"lvl": "INFO", "corr": null, "trans": null, "op": null, '
                '"comp": "tests_basic_config", "msg": "Msg", "key": "extra"}')), call('\n')])
        else:
            open_mock.assert_called_once_with('/test/fake_file.log', 'a', 'UTF-8')
            open_mock.return_value.write.assert_called_once_with(RegexpMatch(
                '{"time": "[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}Z", '
                '"lvl": "INFO", "corr": null, "trans": null, "op": null, '
                '"comp": "tests_basic_config", "msg": "Msg", "key": "extra"}\n'))

    def test_json_formater_with_transaction(self):
        with self.patch_open as open_mock:
            file_handler = FileHandler('/test/fake_file.log', encoding='UTF-8')
            file_handler.addFilter(TrackingFilter())
            file_handler.setFormatter(JsonFormatter())
            logging.basicConfig()
            test_logger = logging.getLogger("test")
            test_logger.addHandler(file_handler)
            test_logger.setLevel(logging.DEBUG)
            local_context.trans = "trans"
            local_context.corr = "corr"
            local_context.op = "op"
            test_logger.info("Msg1")
            test_logger.debug("Msg2")
            test_logger.error("Msg3")
            if six.PY3:
                open_mock.assert_called_once_with('/test/fake_file.log', 'a', encoding='UTF-8')
                open_mock.return_value.write.assert_has_calls([
                    call(RegexpMatch('{"time": "[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}Z", '
                                     '"lvl": "INFO", "corr": "corr", "trans": "trans", "op": "op", '
                                     '"comp": "tests_basic_config", "msg": "Msg1"}')), call('\n'),
                    call(RegexpMatch('{"time": "[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}Z", '
                                     '"lvl": "DEBUG", "corr": "corr", "trans": "trans", "op": "op", '
                                     '"comp": "tests_basic_config", "msg": "Msg2"}')), call('\n'),
                    call(RegexpMatch('{"time": "[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}Z", '
                                     '"lvl": "ERROR", "corr": "corr", "trans": "trans", "op": "op", '
                                     '"comp": "tests_basic_config", "msg": "Msg3"}')),  call('\n')
                ])
            else:
                open_mock.assert_called_once_with('/test/fake_file.log', 'a', 'UTF-8')
                open_mock.return_value.write.assert_has_calls([
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
