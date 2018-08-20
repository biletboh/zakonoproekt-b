from django.test import TestCase

from committees.models import Committee
from committees.serializers import CommitteeSerializer
from committees.tests.test_models import CommitteeDataMixin


class CommitteeSerializerTestCase(CommitteeDataMixin, TestCase):
    """Test the Initiator serializer."""

    def setUp(self):
        super().setUp()
        committee = Committee.objects.create(**self.committee_data)
        self.serializer = CommitteeSerializer(instance=committee)

    def test_fields(self):
        """Test serializer fields."""

        data = self.serializer.data
        keys = ['id', 'title', 'head', 'description', 'number', 'website',
                'secretary', 'secretary_contacts']
        self.assertCountEqual(data.keys(), keys)
