from unittest.mock import MagicMock

from django.core.files import File
from django.core.management import call_command
from django.test import TestCase

from core.mixins import BaseTestDataMixin
from initiators.models import Initiator, Convocation
from committees.models import Committee
from committees.tests.test_models import CommitteeDataMixin


class ConvocationDataMixin(BaseTestDataMixin):
    """Mixin that adds Convocation data."""

    def setUp(self):
        self.convocation_data = {
            'number': 8,
            'latin_number': 'VIII скликання'
        }


class ConvocationFixturesMixin(BaseTestDataMixin):

    def setUp(self):
        call_command('loaddata', 'initiators/tests/fixtures/convocations',
                     verbosity=0)


class InitiatorDataMixin(CommitteeDataMixin, ConvocationFixturesMixin,
                         BaseTestDataMixin):
    """Mixin that adds Initiator data."""

    def setUp(self):
        ConvocationFixturesMixin.setUp(self)
        CommitteeDataMixin.setUp(self)
        mock_file = MagicMock(spec=File, name='FileMock.txt')
        mock_file.name = 'test.jpg'
        self.committee = Committee.objects.create(**self.committee_data)
        self.initiator_data = {
            'first_name': 'Тест',
            'last_name': 'Тестенко',
            'middle_name': 'Тестович',
            'convocation_by_number': 8,
            'party': 'Безпартійний',
            'person_id': 18003,
            'rada_id': 180,
            'faction': 'Позафракційний',
            'information': 'Інформація',
            'email': 'someemail@test.com',
            'phone': '+3809903391212',
            'photo': mock_file,
            'committees_by_title': self.committee.title
        }


class InitiatorModelTestCase(InitiatorDataMixin, TestCase):
    """Test the Initiator model."""

    def setUp(self):
        super().setUp()
        self.photo_url = 'http://static.rada.gov.ua/dep_img8/d207_1.jpg'

    def test_can_create(self):
        """Test if the model can create a object."""

        old_count = Initiator.objects.count()
        Initiator.objects.create(**self.initiator_data)
        new_count = Initiator.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_str(self):
        """Test a string representation of the model."""

        test_object = Initiator.objects.create(**self.initiator_data)
        test_repr = (self.initiator_data['first_name']
                     + ' ' + self.initiator_data['last_name'])
        self.assertEqual(str(test_object), test_repr)

    def test_photo_save(self):
        """Test if the model can save photo of an object."""

        self.initiator_data.pop('photo', None)
        i = Initiator.objects.create(**self.initiator_data)
        i.save_photo(self.photo_url)
        self.assertTrue(bool(i.photo))

    def test_has_committees(self):
        """Test if the object has committees."""

        initiator = Initiator.objects.create(**self.initiator_data)
        count = initiator.committees.count()
        self.assertNotEqual(count, 0)

    def test_has_convocations(self):
        """Test if the object has convocations."""

        initiator = Initiator.objects.create(**self.initiator_data)
        count = initiator.convocations.count()
        self.assertNotEqual(count, 0)


class ConvocationModelTestCase(ConvocationDataMixin, TestCase):
    """Test the Convocation model."""

    def test_can_create(self):
        """Test if the model can create a object."""

        old_count = Convocation.objects.count()
        Convocation.objects.create(**self.convocation_data)
        new_count = Convocation.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_str(self):
        """Test a string representation of the model."""

        test_object = Convocation.objects.create(**self.convocation_data)
        test_repr = self.convocation_data['latin_number']
        self.assertEqual(str(test_object), test_repr)
