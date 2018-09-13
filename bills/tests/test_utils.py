import json
import os

from django.conf import settings
from django.test import TestCase

from bills.models import Bill
from bills.utils import BillParser
from initiators.tests.test_models import ConvocationFixturesMixin


class BillParserModelTestCase(ConvocationFixturesMixin, TestCase):
    """Test the BillParser helper class."""

    def setUp(self):
        super().setUp()
        self.raw_data = json.load(
            open(os.path.join(settings.BASE_DIR,
                              'bills/tests/bill_parse_data.json')))
        self.bill1_raw_data = self.raw_data[3]
        self.parser = BillParser()
        self.maxDiff = None

    def test_parser(self):
        """Test if Parser can prapare bill data."""

        parsed_data = self.parser.parse(self.raw_data[3])
        keys = ['title', 'bill_id', 'number', 'convocation', 'session',
                'rubric', 'subject', 'bill_type', 'phase', 'phase_date',
                'uri', 'agenda', 'registration_date', 'chronology',
                'documents', 'committees', 'authors', 'initiators',
                'executives', 'main_executives', 'bind_bills', 'alternatives'
                ]

        self.assertCountEqual(parsed_data.keys(), keys)

    def test_initiator_parser_single(self):
        """Test if Parser can prepare an initiator data."""

        parsed_data = self.parser.parse_initiators(
            self.raw_data[3]['initiators'])
        keys = ['person_id', 'first_name', 'last_name', 'middle_name',
                'committees_by_title', 'convocation_by_latin_number',
                'post', 'organization']
        self.assertCountEqual(parsed_data[0].keys(), keys)

    def test_initiator_parser_multiple(self):
        """Test if Parser can prepare numerous initiators data."""

        parsed_data = self.parser.parse_initiators(
            self.raw_data[3]['initiators'])
        keys = ['person_id', 'first_name', 'last_name', 'middle_name',
                'committees_by_title', 'convocation_by_latin_number',
                'post', 'organization']
        self.assertCountEqual(parsed_data[0].keys(), keys)
        self.assertGreater(len(parsed_data), 1)

    def test_initiator_parser_outer(self):
        """Test if Parser can prepare initiators with 'outer' key in data."""

        parsed_data = self.parser.parse_initiators(
            self.raw_data[4]['initiators'])
        keys = ['person_id', 'first_name', 'last_name', 'middle_name',
                'committees_by_title', 'convocation_by_latin_number',
                'post', 'organization']
        self.assertCountEqual(parsed_data[0].keys(), keys)

    def test_executive_parser_single(self):
        """Test if Parser can prepare executives data."""

        parsed_data = self.parser.parse_executives(
            self.raw_data[6]['executives'])
        keys = ['person_id', 'first_name', 'last_name', 'middle_name',
                'committees_by_title']
        self.assertCountEqual(parsed_data[0].keys(), keys)
        self.assertEqual(len(parsed_data), 1)

    def test_executive_parser_multiple(self):
        """Test if Parser can prepare executives data."""

        parsed_data = self.parser.parse_executives(
            self.raw_data[3]['executives'])
        keys = ['person_id', 'first_name', 'last_name', 'middle_name',
                'committees_by_title']
        self.assertCountEqual(parsed_data[0].keys(), keys)
        self.assertGreater(len(parsed_data), 1)

    def test_main_executive_parser(self):
        """Test if Parser can prepare main executives data."""

        parsed_data = self.parser.parse_main_executives(
            self.raw_data[3]['mainExecutives'])
        keys = ['person_id', 'first_name', 'last_name', 'middle_name',
                'committees_by_title']
        self.assertCountEqual(parsed_data[0].keys(), keys)

    def test_documents_parser_multiple(self):
        """Test if Parser can prepare documents data with multiple items."""

        parsed_data = self.parser.parse_documents(
            self.raw_data[3]['documents'])
        keys = ['document_type', 'date', 'uri']
        self.assertCountEqual(parsed_data[0].keys(), keys)
        self.assertGreater(len(parsed_data), 1)

    def test_documents_parser_single(self):
        """Test if Parser can prepare documents data with single item."""

        parsed_data = self.parser.parse_documents(
            self.raw_data[3]['documents'])
        keys = ['document_type', 'date', 'uri']
        self.assertCountEqual(parsed_data[0].keys(), keys)

    def test_documents_parser_workflow(self):
        """Test if Parser can prepare documents data with workflow root."""

        parsed_data = self.parser.parse_documents(
            self.raw_data[8]['documents'])
        keys = ['document_type', 'date', 'uri']
        self.assertCountEqual(parsed_data[0].keys(), keys)

    def test_documents_parser_source(self):
        """Test if Parser can prepare documents data with source root."""

        parsed_data = self.parser.parse_documents(
            self.raw_data[2]['documents'])
        keys = ['document_type', 'date', 'uri']
        self.assertCountEqual(parsed_data[0].keys(), keys)

    def test_documents_parser_workflow_source(self):
        """Test if Parser can prepare documents data with workflow root."""

        parsed_data = self.parser.parse_documents(
            self.raw_data[9]['documents'])
        keys = ['document_type', 'date', 'uri']
        self.assertCountEqual(parsed_data[0].keys(), keys)

    def test_prepare_committees_multiple(self):
        """Test if Parser can prepare committees data of complex structure."""

        parsed_data = self.parser.prepare_committees(
            self.raw_data[5]['workOuts'])
        keys = ['title', 'date_got', 'date_passed']
        self.assertCountEqual(parsed_data[0].keys(), keys)
        self.assertGreater(len(parsed_data), 1)

    def test_prepare_committees_single(self):
        """Test if Parser can prepare committees data of complex structure."""

        parsed_data = self.parser.prepare_committees(
            self.raw_data[3]['workOuts'])
        keys = ['title', 'date_got', 'date_passed']
        self.assertCountEqual(parsed_data[0].keys(), keys)

    def test_committee_parser_multiple(self):
        """Test if Parser can prepare numerous committees data."""

        parsed_data = self.parser.parse_committees(
            self.raw_data[3]['workOuts'])
        keys = ['title', 'date_got', 'date_passed']
        self.assertCountEqual(parsed_data[0].keys(), keys)
        self.assertGreater(len(parsed_data), 1)

    def test_committee_parser_single(self):
        """Test if Parser can prepare numerous committees data."""

        parsed_data = self.parser.parse_committees(
            self.raw_data[3]['workOuts'])
        keys = ['title', 'date_got', 'date_passed']
        self.assertCountEqual(parsed_data[0].keys(), keys)

    def test_bills_parser_multiple(self):
        """Test if Parser can prepare multiple bind bills data items."""

        parsed_data = self.parser.parse_bills(
            self.raw_data[3]['alternative'])
        keys = ['bill_id']
        self.assertCountEqual(parsed_data[0].keys(), keys)

    def test_bills_parser_single(self):
        """Test if Parser can prepare bind bills data with single item."""

        parsed_data = self.parser.parse_bills(
            self.raw_data[7]['alternative'])
        keys = ['bill_id']
        self.assertCountEqual(parsed_data[0].keys(), keys)
        self.assertEqual(len(parsed_data), 1)

    def test_bind_bills_parser_single(self):
        """Test if Parser can prepare bill alternatives data."""

        parsed_data = self.parser.parse_bills(
            self.raw_data[3]['bind'])
        keys = ['bill_id']
        self.assertCountEqual(parsed_data[0].keys(), keys)
        self.assertEqual(len(parsed_data), 1)

    def test_bind_bills_parser_multiple(self):
        """Test if Parser can prepare bill alternatives data."""

        parsed_data = self.parser.parse_bills(
            self.raw_data[3]['bind'])
        keys = ['bill_id']
        self.assertCountEqual(parsed_data[0].keys(), keys)

    def test_can_create(self):
        """Test if the Bill model can create a object out of the parsed
        data."""

        old_count = Bill.objects.count()
        parsed_data = self.parser.parse(self.raw_data[3])
        Bill.objects.create(**parsed_data)
        new_count = Bill.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_has_authors(self):
        """Test if the object has authors."""

        parser = BillParser()
        parsed_data = parser.parse(self.raw_data[3])
        bill = Bill.objects.create(**parsed_data)
        count = bill.authors.count()
        self.assertNotEqual(count, 0)

    def test_has_initiators(self):
        """Test if the object has initiators."""

        parser = BillParser()
        parsed_data = parser.parse(self.raw_data[3])
        bill = Bill.objects.create(**parsed_data)
        count = bill.initiators.count()
        self.assertNotEqual(count, 0)

    def test_has_executives(self):
        """Test if the object has executives."""

        parser = BillParser()
        parsed_data = parser.parse(self.raw_data[3])
        bill = Bill.objects.create(**parsed_data)
        count = bill.executives.count()
        self.assertNotEqual(count, 0)

    def test_has_main_executives(self):
        """Test if the object has main executives."""

        parser = BillParser()
        parsed_data = parser.parse(self.raw_data[3])
        bill = Bill.objects.create(**parsed_data)
        count = bill.main_executives.count()
        self.assertNotEqual(count, 0)

    def test_has_passings(self):
        """Test if the object has passings (chronology)."""

        parser = BillParser()
        parsed_data = parser.parse(self.raw_data[3])
        bill = Bill.objects.create(**parsed_data)
        count = bill.chronology.count()
        self.assertNotEqual(count, 0)

    def test_has_documents(self):
        """Test if the object has documents."""

        parser = BillParser()
        parsed_data = parser.parse(self.raw_data[3])
        bill = Bill.objects.create(**parsed_data)
        count = bill.documents.count()
        self.assertNotEqual(count, 0)

    def test_has_committees(self):
        """Test if the object has committees."""

        parser = BillParser()
        parsed_data = parser.parse(self.raw_data[3])
        bill = Bill.objects.create(**parsed_data)
        count = bill.committees.count()
        self.assertNotEqual(count, 0)

    def test_has_bind_bills(self):
        """Test if the object has related bill ids."""

        parser = BillParser()
        parsed_data = parser.parse(self.raw_data[0])
        Bill.objects.create(**parsed_data)
        parsed_data = parser.parse(self.raw_data[1])
        Bill.objects.create(**parsed_data)
        parsed_data = parser.parse(self.raw_data[2])
        bill = Bill.objects.create(**parsed_data)
        count = bill.bind_bills.count()
        self.assertNotEqual(count, 0)

    def test_has_alternatives(self):
        """Test if the object has related bill ids."""

        parser = BillParser()
        parsed_data = parser.parse(self.raw_data[0])
        Bill.objects.create(**parsed_data)
        parsed_data = parser.parse(self.raw_data[1])
        Bill.objects.create(**parsed_data)
        parsed_data = parser.parse(self.raw_data[2])
        Bill.objects.create(**parsed_data)
        parsed_data = parser.parse(self.raw_data[3])
        bill = Bill.objects.create(**parsed_data)
        count = bill.alternatives.count()
        self.assertNotEqual(count, 0)

    def test_none_to_str(self):
        """Test if method transforms None to empty string."""

        value = None
        parser = BillParser()
        result = parser.none_to_str(value)
        self.assertEqual(result, '')

    def test_parse_root(self):
        """Test if method transform dict key to a list."""

        root = {'date': '2015-01-29'}
        list_root = [{'date': '2015-01-29'}]
        parser = BillParser()
        result = parser.parse_root(root)
        self.assertTrue(type(result) is list)
        self.assertEqual(result, list_root)
