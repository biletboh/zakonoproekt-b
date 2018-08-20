from unittest.mock import patch, MagicMock

from django.test import TestCase

from bills.models import Bill, Passing, Document, AgendaQuestion, WorkOuts
from bills.serializers import BillSerializer, PassingSerializer,\
    DocumentSerializer, AgendaSerializer, WorkOutsSerializer
from bills.tests.test_models import BillDataMixin, PassingDataMixin,\
    DocumentDataMixin, AgendaDataMixin, WorkOutsDataMixin
from committees.models import Committee
from committees.tests.test_models import CommitteeDataMixin


class BillSerializerTestCase(BillDataMixin, TestCase):
    """Test the Initiator serializer."""

    def setUp(self):
        super().setUp()
        bill = Bill.objects.create(**self.bill_data)
        self.serializer = BillSerializer(instance=bill)

    def test_fields(self):
        """Test serializer fields."""

        data = self.serializer.data
        keys = ['id', 'title', 'rada_id', 'uri', 'number', 'convocation',
                'session', 'rubric', 'subject', 'bill_type', 'phase',
                'phase_date', 'registration_date', 'agenda_number',
                'agenda_last_date', 'agenda_uri', 'committee_date_passed',
                'bind_bills', 'alternatives', 'authors', 'executives',
                'main_executives', 'chronology', 'committees', 'documents']
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
        keys = ['id', 'bill', 'document_type', 'date', 'uri', 'document_file']
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
        CommitteeDataMixin.setUp(self)
        WorkOutsDataMixin.setUp(self)
        bill = Bill.objects.create(**self.bill_data)
        committee = Committee.objects.create(**self.committee_data)
        self.workouts_data['bill'] = bill
        self.workouts_data['committee'] = committee
        workout = WorkOuts.objects.create(**self.workouts_data)
        self.serializer = WorkOutsSerializer(instance=workout)

    def test_fields(self):
        """Test serializer fields."""

        data = self.serializer.data
        keys = ['id', 'title', 'date_passed', 'date_got', 'bill', 'committee']
        self.assertCountEqual(data.keys(), keys)
