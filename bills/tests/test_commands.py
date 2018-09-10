import json
import os
from unittest.mock import patch

from django.test import TestCase
from django.core import management
from django.conf import settings

from bills.models import Bill


class LoadDataCommandTestCase(TestCase):
    """Test the Initiator Commands."""

    def setUp(self):
        super().setUp()
        patcher_dowload_data = patch('bills.management.commands'
                                     + '.load_bills.Command.download_data')
        self.mock_download_data = patcher_dowload_data.start()
        self.addCleanup(patcher_dowload_data.stop)
        self.bills_data = json.load(
            open(os.path.join(settings.BASE_DIR,
                              'bills/tests/bills_data.json')))

    def test_command(self):
        """Test if the command loads bills."""

        self.mock_download_data.return_value = 200, self.bills_data
        management.call_command('load_bills')
        count = Bill.objects.count()
        self.assertGreater(count, 0)
