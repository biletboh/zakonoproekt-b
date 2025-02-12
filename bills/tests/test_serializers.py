from unittest.mock import patch, MagicMock

from django.test import TestCase
from django.test.client import RequestFactory

from rest_framework.reverse import reverse

from bills.models import Bill, Passing, Document, AgendaQuestion, WorkOuts
from bills.serializers import BillSerializer, PassingSerializer,\
    DocumentSerializer, AgendaSerializer, WorkOutsSerializer
from bills.tests.test_models import BillDataMixin, PassingDataMixin,\
    DocumentDataMixin, AgendaDataMixin, WorkOutsDataMixin


class BillSerializerTestCase(BillDataMixin, TestCase):
    """Test the Initiator serializer."""

    def setUp(self):
        super().setUp()
        bill = Bill.objects.create(**self.bill_data)
        self.rf = RequestFactory()
        request = self.rf.get(reverse('bills-list'))
        self.serializer = BillSerializer(instance=bill,
                                         context={'request': request})

    def test_fields(self):
        """Test serializer fields."""

        data = self.serializer.data
        keys = ['id', 'title', 'bill_id', 'uri', 'number', 'convocation',
                'session', 'rubric', 'subject', 'bill_type', 'phase',
                'phase_date', 'registration_date', 'agenda_number',
                'agenda_last_date', 'agenda_uri', 'bind_bills',
                'alternatives', 'authors', 'executives', 'main_executives',
                'initiators', 'chronology', 'committees', 'documents', 'url']
        self.assertCountEqual(data.keys(), keys)

    @patch('bills.models.Bill.objects.create', MagicMock(name='create'))
    def test_create(self):
        """Test serializer create method."""

        serializer = BillSerializer(data=self.bill_data)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)

        self.assertTrue(Bill.objects.create.called)
        self.assertEqual(Bill.objects.create.call_count, 1)


class PassingSerializerTestCase(PassingDataMixin, TestCase):
    """Test the Initiator serializer."""

    def setUp(self):
        super().setUp()
        passing = Passing.objects.create(**self.passing_data)
        self.serializer = PassingSerializer(instance=passing)

    def test_fields(self):
        """Test serializer fields."""

        data = self.serializer.data
        keys = ['id', 'title', 'date']
        self.assertCountEqual(data.keys(), keys)


class DocumentSerializerTestCase(BillDataMixin, TestCase):
    """Test the Initiator serializer."""

    def setUp(self):
        DocumentDataMixin.setUp(self)
        BillDataMixin.setUp(self)
        bill = Bill.objects.create(**self.bill_data)
        self.document_data['bill'] = bill
        document = Document.objects.create(**self.document_data)
        self.serializer = DocumentSerializer(instance=document)

    def test_fields(self):
        """Test serializer fields."""

        data = self.serializer.data
        keys = ['id', 'document_type', 'date', 'uri', 'document_file']
        self.assertCountEqual(data.keys(), keys)


class AgendaSerializerTestCase(AgendaDataMixin, TestCase):
    """Test the Agenda serializer."""

    def setUp(self):
        super().setUp()
        agenda = AgendaQuestion.objects.create(**self.agenda_data)
        self.serializer = AgendaSerializer(instance=agenda)

    def test_fields(self):
        """Test serializer fields."""

        data = self.serializer.data
        keys = ['id', 'bills', 'title', 'question_type', 'id_event',
                'vote_for', 'vote_against', 'vote_abstain', 'not_voting',
                'present', 'absent', 'total']
        self.assertCountEqual(data.keys(), keys)


class WorkOutsSerializerTestCase(BillDataMixin, TestCase):
    """Test the WorkOut serializer."""

    def setUp(self):
        BillDataMixin.setUp(self)
        WorkOutsDataMixin.setUp(self)
        bill = Bill.objects.create(**self.bill_data)
        self.workouts_data['bill'] = bill
        self.workouts_data['committee'] = self.committee
        workout = WorkOuts.objects.create(**self.workouts_data)
        self.serializer = WorkOutsSerializer(instance=workout)

    def test_fields(self):
        """Test serializer fields."""

        data = self.serializer.data
        keys = ['id', 'title', 'date_passed', 'date_got']
        self.assertCountEqual(data.keys(), keys)
