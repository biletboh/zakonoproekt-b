from django.test import TestCase
from django.core import management

from initiators.models import Initiator
from initiators.tests.test_models import InitiatorDataMixin


class LoadDataCommandTestCase(InitiatorDataMixin, TestCase):
    """Test the Initiator Commands."""

    def test_command(self):
        """Test if the command loads initiators."""

        management.call_command('load_initiators')
        count = Initiator.objects.count()
        self.assertGreater(count, 0)
