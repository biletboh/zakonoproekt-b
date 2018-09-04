from django.test import TestCase
from django.test.client import RequestFactory

from rest_framework.reverse import reverse

from committees.models import Committee
from committees.serializers import CommitteeSerializer
from committees.tests.test_models import CommitteeDataMixin


class CommitteeSerializerTestCase(CommitteeDataMixin, TestCase):
    """Test the Initiator serializer."""

    def setUp(self):
        super().setUp()
        committee = Committee.objects.create(**self.committee_data)
        self.rf = RequestFactory()
        request = self.rf.get(reverse('committees-list'))
        self.serializer = CommitteeSerializer(
            instance=committee, context={'request': request})

    def test_fields(self):
        """Test serializer fields."""

        data = self.serializer.data
        keys = ['id', 'title', 'head', 'description', 'number', 'website',
                'secretary', 'secretary_contacts', 'url']
        self.assertCountEqual(data.keys(), keys)
