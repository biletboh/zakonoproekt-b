from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from bills.models import Bill
from bills.serializers import BillSerializer
from bills.tests.test_models import BillDataMixin, DocumentDataMixin,\
    WorkOutsDataMixin, PassingDataMixin
from committees.models import Committee
from committees.tests.test_models import CommitteeDataMixin
from initiators.tests.test_models import InitiatorDataMixin


class BillCRUDTestCase(BillDataMixin, APITestCase):
    """Test suite for the api views."""

    def setUp(self):
        BillDataMixin.setUp(self)
        PassingDataMixin.setUp(self)
        InitiatorDataMixin.setUp(self)
        DocumentDataMixin.setUp(self)
        CommitteeDataMixin.setUp(self)
        WorkOutsDataMixin.setUp(self)
        Committee.objects.create(**self.committee_data)
        self.initiator_data.pop('photo', None)
        self.initiator_data2 = self.initiator_data.copy()
        self.initiator_data2['last_name'] = 'Тестун'
        self.initiator_data2['rada_id'] = 13009
        self.bill_data['chronology'] = [self.passing_data, self.passing_data]
        self.bill_data['authors'] = [self.initiator_data, self.initiator_data2]
        self.bill_data['initiators'] = [self.initiator_data,
                                        self.initiator_data2]
        self.bill_data['executives'] = [self.initiator_data,
                                        self.initiator_data2]
        self.bill_data['main_executives'] = [self.initiator_data,
                                             self.initiator_data2]
        self.bill_data['documents'] = [self.document_data]
        self.bill_data['committees'] = [self.workouts_data]
        self.bill_invalid_data = {
            'invalid': 'data'
        }
        self.user = User.objects.create_user('test', 'test@zakonoproekt.com',
                                             'testpass10')

    def test_create(self):
        """Test the Bill creation endpoint."""

        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('bills-list'),
                                    self.bill_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_data(self):
        """Test the Bill creation endpoint with invalid data."""

        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('bills-list'),
                                    self.bill_invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list(self):
        """Test the Bill list endpoint."""

        Bill.objects.create(**self.bill_data)
        bills = Bill.objects.all()
        serializer = BillSerializer(bills, many=True)

        response = self.client.get(reverse('bills-list'))
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve(self):
        """Test the Bill list endpoint."""

        bill = Bill.objects.create(**self.bill_data)
        serializer = BillSerializer(bill)

        response = self.client.get(
            reverse('bills-detail', kwargs={'pk': bill.pk}))
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_destroy(self):
        """Test the Bill delete endpoint."""

        self.client.force_authenticate(user=self.user)
        bill = Bill.objects.create(**self.bill_data)
        response = self.client.delete(
            reverse('bills-detail', kwargs={'pk': bill.pk}), format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_permissions_destroy(self):
        """Test the Bill delete endpoint premissions."""

        Bill.objects.create(**self.bill_data)
        response = self.client.delete(
            reverse('bills-detail', kwargs={'pk': 1}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_permissions_create(self):
        """Test the Bill creation endpoint premissions."""

        response = self.client.post(reverse('bills-list'),
                                    self.bill_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_permissions_update(self):
        """Test the Bill creation update premissions."""

        Bill.objects.create(**self.bill_data)
        response = self.client.put(
            reverse('bills-detail', kwargs={'pk': 1}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_permissions_partial_update(self):
        """Test the Bill creation update premissions."""

        Bill.objects.create(**self.bill_data)
        response = self.client.patch(
            reverse('bills-detail', kwargs={'pk': 1}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
