from django.test import TestCase
from django.test.client import RequestFactory

from rest_framework.reverse import reverse

from initiators.models import Initiator
from initiators.serializers import InitiatorSerializer
from initiators.tests.test_models import InitiatorDataMixin


class InitiatorSerializerTestCase(InitiatorDataMixin, TestCase):
    """Test the Initiator serializer."""

    def setUp(self):
        super().setUp()
        self.initiator = Initiator.objects.create(**self.initiator_data)
        self.rf = RequestFactory()
        request = self.rf.get(reverse('initiators-list'))
        self.serializer = InitiatorSerializer(instance=self.initiator,
                                              context={'request': request})

    def test_fields(self):
        """Test serialiser fields."""

        data = self.serializer.data
        keys = ['id', 'first_name', 'last_name', 'middle_name', 'convocation',
                'party', 'faction', 'information', 'email', 'phone', 'photo',
                'rada_id', 'url']
        self.assertCountEqual(data.keys(), keys)
