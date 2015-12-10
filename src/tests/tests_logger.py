import six
from unittest import TestCase
from pylogops import local_context
from pylogops.logger import TrackingFilter

if six.PY3:
    from unittest.mock import MagicMock  # @UnusedImport @UnresolvedImport
else:
    from mock import MagicMock  # @Reimport


class TestLogger(TestCase):

    def test_tracking_filter(self):
        record_mock = MagicMock(name='log_mock')
        local_context.transaction_id = 'test_id'
        local_context.correlator_id = 'correlator_id'
        local_context.op_type = 'op_type'
        track_filter = TrackingFilter()
        res = track_filter.filter(record_mock)
        self.assertEquals(True, res, 'Tracking filter not executed correctly')
        self.assertEquals(record_mock.transaction_id, 'test_id')
        self.assertEquals(record_mock.correlator_id, 'correlator_id')
        self.assertEquals(record_mock.op_type, 'op_type')
