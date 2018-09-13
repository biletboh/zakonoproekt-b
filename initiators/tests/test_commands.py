from django.test import TestCase
from django.core import management

from initiators.models import Initiator, Convocation
from initiators.tests.test_models import ConvocationDataMixin


class LoadDataCommandTestCase(ConvocationDataMixin, TestCase):
    """Test the Initiator Commands."""

    def setUp(self):
        super().setUp()
        Convocation.objects.create(**self.convocation_data)

    def test_command(self):
        """Test if the command loads initiators."""

        management.call_command('load_initiators')
        count = Initiator.objects.count()
        self.assertGreater(count, 0)
