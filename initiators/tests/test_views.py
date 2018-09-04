from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from initiators.models import Initiator
from initiators.serializers import InitiatorSerializer
from initiators.tests.test_models import InitiatorDataMixin


class InitiatorCRUDTestCase(InitiatorDataMixin, APITestCase):
    """Test suite for the Initiator api views."""

    def setUp(self):
        super().setUp()
        self.initiator_data.pop('photo', None)
        self.initiator_data2 = self.initiator_data.copy()
        self.initiator_data2['last_name'] = 'Тестун'
        self.initiator_data2['rada_id'] = 13009
        self.initiator_invalid_data = {
            'invalid': 'data'
        }
        self.user = User.objects.create_user('test', 'test@zakonoproekt.com',
                                             'testpass10')

    def test_create(self):
        """Test the Initiator creation endpoint."""

        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('initiators-list'),
                                    self.initiator_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_data(self):
        """Test the Initiator creation endpoint with invalid data."""

        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('initiators-list'),
                                    self.initiator_invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list(self):
        """Test the Initiator list endpoint."""

        Initiator.objects.create(**self.initiator_data)
        initiators = Initiator.objects.all()
        serializer = InitiatorSerializer(initiators, many=True)

        response = self.client.get(reverse('initiators-list'))
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve(self):
        """Test the Initiator list endpoint."""

        initiator = Initiator.objects.create(**self.initiator_data)
        serializer = InitiatorSerializer(initiator)

        response = self.client.get(
            reverse('initiators-detail', kwargs={'pk': initiator.pk}))
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_destroy(self):
        """Test the Initiator delete endpoint."""

        self.client.force_authenticate(user=self.user)
        initiator = Initiator.objects.create(**self.initiator_data)
        response = self.client.delete(
            reverse('initiators-detail', kwargs={'pk': initiator.pk}),
            format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_permissions_destroy(self):
        """Test the Initiator delete endpoint premissions."""

        Initiator.objects.create(**self.initiator_data)
        response = self.client.delete(
            reverse('initiators-detail', kwargs={'pk': 1}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_permissions_create(self):
        """Test the Initiator creation endpoint premissions."""

        response = self.client.post(reverse('initiators-list'),
                                    self.initiator_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_permissions_update(self):
        """Test the Initiator creation update premissions."""

        Initiator.objects.create(**self.initiator_data)
        response = self.client.put(
            reverse('initiators-detail', kwargs={'pk': 1}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_permissions_partial_update(self):
        """Test the Initiator creation update premissions."""

        Initiator.objects.create(**self.initiator_data)
        response = self.client.patch(
            reverse('initiators-detail', kwargs={'pk': 1}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
