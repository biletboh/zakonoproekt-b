from django.test import TestCase
from django.core import management

from committees.models import Committee


class LoadDataCommandTestCase(TestCase):
    """Test the Initiator Commands."""

    def test_command(self):
        """Test if the command loads initiators."""

        management.call_command('load_committees')
        count = Committee.objects.count()
        self.assertGreater(count, 0)
