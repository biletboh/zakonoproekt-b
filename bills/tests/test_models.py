from unittest.mock import MagicMock

from django.test import TestCase
from django.core.files import File

from bills.models import Bill, Passing, Document, AgendaQuestion, WorkOuts
from committees.models import Committee
from committees.tests.test_models import CommitteeDataMixin
from initiators.models import Initiator
from initiators.tests.test_models import InitiatorDataMixin


class BillDataMixin(InitiatorDataMixin):
    """Mixin that adds Bill data."""

    def setUp(self):
        super().setUp()
        self.bill_data = {
            'title': ('про денонсацію Угоди між Урядом Союзу Радянських '
                      + 'Соціалістичних Республік і Урядом Республіки Кіпр '
                      + 'про уникнення подвійного оподаткування доходів та '
                      + 'майна від 29 жовтня 1982 року'),
            'rada_id': 52575,
            'number': '0001',
            'convocation': 8,
            'session': '1 сесія',
            'rubric': 'Двосторонні міжнародні угоди',
            'subject': 'Народний депутат України',
            'registration_date': '2014-12-01',
            'bill_type': 'Проект Закону',
            'phase_date': '2016-02-18',
            'phase': 'Відхилено та знято з розгляду',
            'uri': ('http://w1.c1.rada.gov.ua/pls/zweb2/'
                    + 'webproc4_1?pf3511=52575'),
            'agenda_uri': 'http://zakon.rada.gov.ua/go/37-VIII',
            'agenda_last_date': '2014-12-23',
            'agenda_number': '37-VIII',
        }


class BillModelTestCase(BillDataMixin, InitiatorDataMixin, TestCase):
    """Test the Bill model."""

    def test_can_create(self):
        """Test if the model can create a object."""

        old_count = Bill.objects.count()
        bill = Bill.objects.create(**self.bill_data)
        initiator = Initiator.objects.create(**self.initiator_data)
        bill.authors.add(initiator)
        bill.save()
        new_count = Bill.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_str(self):
        """Test a string representation of the model."""

        test_object = Bill.objects.create(**self.bill_data)
        self.assertEqual(str(test_object), self.bill_data['title'])


class PassingModelTestCase(TestCase):
    """Test the Passing model."""

    def setUp(self):
        self.passing_data = {
            'title': 'В порядок денний не включено',
            'date': '2016-02-03'
        }

    def test_can_create(self):
        """Test if the model can create a object."""

        old_count = Passing.objects.count()
        Passing.objects.create(**self.passing_data)
        new_count = Passing.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_str(self):
        """Test a string representation of the model."""

        test_object = Passing.objects.create(**self.passing_data)
        self.assertEqual(str(test_object), self.passing_data['title'])


class DocumentModelTestCase(BillDataMixin, TestCase):
    """Test the Document model."""

    def setUp(self):
        super().setUp()
        bill = Bill.objects.create(**self.bill_data)
        mock_file = MagicMock(spec=File, name='FileMock.txt')
        mock_file.name = 'test.txt'
        self.document_data = {
            'document_type': 'Проект Закону',
            'date': '2016-02-03',
            'uri': 'http://w1.c1.rada.gov.ua/pls/zweb2/webproc34?id=&pf3511',
            'document_file': mock_file,
            'bill': bill
        }

    def test_can_create(self):
        """Test if the model can create a object."""

        old_count = Document.objects.count()
        Document.objects.create(**self.document_data)
        new_count = Document.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_str(self):
        """Test a string representation of the model."""

        test_object = Document.objects.create(**self.document_data)
        test_repr = (self.document_data['document_type']
                     + ' ' + self.bill_data['title'])
        self.assertEqual(
            str(test_object), test_repr)


class AgendaQuestionModelTestCase(BillDataMixin, TestCase):
    """Test the AgendaQuestion model."""

    def setUp(self):
        super().setUp()
        self.bill = Bill.objects.create(**self.bill_data)
        self.agenda_data = {
            'title': ('Поіменне голосування  про включення до порядку денного'
                      + 'проекту Закону про внесення змін до Закону України '
                      + '\"Про Державний бюджет України на 2018 рік\" щодо '
                      + 'належного фінансового забезпечення державного '
                      + 'сектору вугільної галузі (№8362)'),
            'question_type': 0,
            'id_event': 19928,
            'vote_for': 256,
            'vote_against': 0,
            'vote_abstain': 0,
            'not_voting': 75,
            'present': 331,
            'absent': 92,
            'total': 423
        }

    def test_can_create(self):
        """Test if the model can create a object."""

        old_count = AgendaQuestion.objects.count()
        q = AgendaQuestion.objects.create(**self.agenda_data)
        q.bills.add(self.bill)
        q.save()

        new_count = AgendaQuestion.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_str(self):
        """Test a string representation of the model."""

        test_object = AgendaQuestion.objects.create(**self.agenda_data)
        self.assertEqual(
            str(test_object), self.agenda_data['title'])


class WorkOutsModelTestCase(BillDataMixin, CommitteeDataMixin, TestCase):
    """Test the WorkOuts model."""

    def setUp(self):
        BillDataMixin.setUp(self)
        CommitteeDataMixin.setUp(self)
        bill = Bill.objects.create(**self.bill_data)
        committee = Committee.objects.create(**self.committee_data)
        self.workouts_data = {
            'title': ('Комітет Верховної Ради України з питань податкової та '
                      + 'митної політики'),
            'date_got': '2014-12-11',
            'date_passed': '2014-12-08',
            'bill': bill,
            'committee': committee
        }

    def test_can_create(self):
        """Test if the model can create a object."""

        old_count = WorkOuts.objects.count()
        q = WorkOuts.objects.create(**self.workouts_data)
        q.save()

        new_count = WorkOuts.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_str(self):
        """Test a string representation of the model."""

        test_object = WorkOuts.objects.create(**self.workouts_data)
        test_repr = self.workouts_data['title'] + ' ' + self.bill_data['title']
        self.assertEqual(str(test_object), test_repr)
