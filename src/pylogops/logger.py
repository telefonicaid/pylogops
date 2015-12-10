"""Several utilities for logging in python.
"""

import logging
import time
import six
from pylogops import local_context
try:
    # make this work in py2.6
    from ordereddict import OrderedDict
except ImportError:
    from collections import OrderedDict
# ujson is quick that json but does not support OrderedDicts
# in loads operation the performance difference is not so big ...
from json import JSONEncoder


class TrackingFilter(logging.Filter):
    """Filter to include in record the track records attributes:
        trans (transaction id)
        corr (correlator id)
        op (operation)
    This values should be included in local_context (e.g. with every request)
    and can be used in formatters later.

    from pylogops import local_context
    import uuid
    local_context.trans = uuid.uuid4().hex
    local_context.corr = "corr"

    local_context use thread.local to store values to be shared in all modules that use it.
    """

    def filter(self, record):
        # Add attributes to LogRecord required by Tdaf Formatters
        record.trans = getattr(local_context, 'trans', None)
        record.corr = getattr(local_context, 'corr', None)
        record.op = getattr(local_context, 'op', None)
        return True


class JsonFormatter(logging.Formatter, object):
    """Overrides Formatter to log messages in json format.
    It defines an ordered list of LogRecord fields to be serialized in json; the
    output name of the fields can also be specified as it is common to change it (e.g.
    Use message field of record and output as msg).

    The time in recors is generated in UTC format.

    When an attribute (dictionary) with name 'additional' exists in LogRecord, all the fields
    will be included in serialization as well. This additional dict can be included in logging
    using the extra keyword.
    The same applies with exc_text field when the log
    record has exception information.

    When this formatter is configured you will have the following outputs:

    logger.info("Output message")
    {"time": "2015-07-08T13:10:03.955Z", "lvl": "INFO", "corr": "bf0fdcc352a94156a423ba152b634ae9",
        "trans": "24ffdbb48ab942f09299b277e1b39e55", "op": "AddAlarms", "comp": "middlewares",
        "msg": "Output message"}

    logger.info("Output message", extra={"additional": {"key": "extra_key"}})
    {"time": "2015-07-08T13:10:03.955Z", "lvl": "INFO", "corr": "bf0fdcc352a94156a423ba152b634ae9",
        "trans": "24ffdbb48ab942f09299b277e1b39e55", "op": "AddAlarms", "comp": "middlewares",
        "msg": "Output message", "key": "extra_key"}
    """

    converter = time.gmtime
    keys_fmt = [('time', 'utctime'), ('lvl', 'levelname'),
                ('corr', 'corr'), ('trans', 'trans'),
                ('op', 'op'), ('comp', 'module'), ('msg', 'message')]

    def __init__(self, converter=None, remove_blanks=False, keys_fmt=None):
        if converter:
            self.converter = converter
        if keys_fmt and isinstance(keys_fmt, list):
            self.keys_fmt = keys_fmt
        self.remove_blanks = remove_blanks
        self._keys_fmt = OrderedDict(self.keys_fmt)
        self.json_encoder = JSONEncoder()
        super(JsonFormatter, self).__init__(fmt=None, datefmt='%Y-%m-%dT%H:%M:%S')

    def encode(self, record_dict):
        try:
            return self.json_encoder.encode(record_dict)
        except Exception as e:
            # In the situations where encode does not work, don't raise any exception
            # that may stop the program; it is better to avoid logging
            raise Exception("Error encoding log entry into JSON: {0}".format(str(e)))

    def format(self, record):
        # Get message and time
        record.message = record.getMessage()
        record.asctime = self.formatTime(record, self.datefmt)
        record.utctime = "{0}.{1:03.0f}Z".format(record.asctime, record.msecs)

        # Serialize record keys to json (just the configured ones and extra)
        record_dict = OrderedDict([(key, getattr(record, log_key, None))
                                   for key, log_key in six.iteritems(self._keys_fmt)])
        if hasattr(record, 'additional') and record.additional:
            record_dict.update(record.additional.items())
        # Add exception info (if available)
        if record.exc_info:
            record.exc_text = self.formatException(record.exc_info)
            record_dict.update({'exc_text': record.exc_text})
        # Remove blanks items
        if self.remove_blanks:
            empty_keys = [k for k, v in six.iteritems(record_dict) if not v]
            for key in empty_keys:
                del record_dict[key]

        return self.encode(record_dict)
