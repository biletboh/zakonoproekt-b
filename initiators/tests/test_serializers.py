from django.test import TestCase

from initiators.models import Initiator
from initiators.serializers import InitiatorSerializer
from initiators.tests.test_models import InitiatorDataMixin


class InitiatorSerializerTestCase(InitiatorDataMixin, TestCase):
    """Test the Initiator serializer."""

    def setUp(self):
        super().setUp()
        self.initiator = Initiator.objects.create(**self.initiator_data)
        self.serializer = InitiatorSerializer(instance=self.initiator)

    def test_fields(self):
        """Test serialiser fields."""

        data = self.serializer.data
        keys = ['id', 'first_name', 'last_name', 'middle_name', 'convocation',
                'party', 'faction', 'information', 'email', 'phone', 'photo']
        self.assertCountEqual(data.keys(), keys)
