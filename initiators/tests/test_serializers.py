from django.test import TestCase
from django.test.client import RequestFactory

from rest_framework.reverse import reverse

from initiators.models import Initiator, Convocation
from initiators.serializers import InitiatorSerializer, ConvocationSerializer
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
        keys = ['id', 'first_name', 'last_name', 'middle_name', 'convocations',
                'party', 'faction', 'information', 'email', 'phone', 'photo',
                'person_id', 'rada_id', 'url', 'committees']
        self.assertCountEqual(data.keys(), keys)


class ConvocationSerializerTestCase(InitiatorDataMixin, TestCase):
    """Test the Convocation serializer."""

    def setUp(self):
        self.convocation_data = {
            'number': 8,
            'latin_number': 'VIII скликання'
        }
        self.convocation = Convocation.objects.create(
            **self.convocation_data)
        self.serializer = ConvocationSerializer(
            instance=self.convocation_data)

    def test_fields(self):
        """Test serialiser fields."""

        data = self.serializer.data
        keys = ['number', 'latin_number']
        self.assertCountEqual(data.keys(), keys)
