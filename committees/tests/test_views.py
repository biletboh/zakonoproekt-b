from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from committees.models import Committee
from committees.serializers import CommitteeSerializer
from committees.tests.test_models import CommitteeDataMixin


class CommitteeCRUDTestCase(CommitteeDataMixin, APITestCase):
    """Test suite for the api views."""

    def setUp(self):
        super().setUp()
        self.committee_invalid_data = {
            'invalid': 'data'
        }
        self.user = User.objects.create_user('test', 'test@zakonoproekt.com',
                                             'testpass10')

    def test_create(self):
        """Test the Committee creation endpoint."""

        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('committees-list'),
                                    self.committee_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_data(self):
        """Test the Committee creation endpoint with invalid data."""

        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('committees-list'),
                                    self.committee_invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list(self):
        """Test the Committee list endpoint."""

        Committee.objects.create(**self.committee_data)
        committees = Committee.objects.all()
        serializer = CommitteeSerializer(committees, many=True)

        response = self.client.get(reverse('committees-list'))
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve(self):
        """Test the Committee list endpoint."""

        committee = Committee.objects.create(**self.committee_data)
        serializer = CommitteeSerializer(committee)

        response = self.client.get(
            reverse('committees-detail', kwargs={'pk': committee.pk}))
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_destroy(self):
        """Test the Committee delete endpoint."""

        self.client.force_authenticate(user=self.user)
        committee = Committee.objects.create(**self.committee_data)
        response = self.client.delete(
            reverse('committees-detail', kwargs={'pk': committee.pk}),
            format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_permissions_destroy(self):
        """Test the Committee delete endpoint premissions."""

        Committee.objects.create(**self.committee_data)
        response = self.client.delete(
            reverse('committees-detail', kwargs={'pk': 1}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_permissions_create(self):
        """Test the Committee creation endpoint premissions."""

        response = self.client.post(reverse('committees-list'),
                                    self.committee_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_permissions_update(self):
        """Test the Committee creation update premissions."""

        Committee.objects.create(**self.committee_data)
        response = self.client.put(
            reverse('committees-detail', kwargs={'pk': 1}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_permissions_partial_update(self):
        """Test the Committee creation update premissions."""

        Committee.objects.create(**self.committee_data)
        response = self.client.patch(
            reverse('committees-detail', kwargs={'pk': 1}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
