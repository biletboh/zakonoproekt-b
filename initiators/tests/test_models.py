from unittest.mock import MagicMock

from django.test import TestCase
from django.core.files import File

from core.mixins import BaseTestDataMixin
from initiators.models import Initiator


class InitiatorDataMixin(BaseTestDataMixin):
    """Mixin that adds Initiator data."""

    def setUp(self):
        mock_file = MagicMock(spec=File, name='FileMock.txt')
        mock_file.name = 'test.jpg'
        self.initiator_data = {
            'first_name': 'Тест',
            'last_name': 'Тестенко',
            'middle_name': 'Тестович',
            'convocation': 8,
            'party': 'Безпартійний',
            'rada_id': 18003,
            'faction': 'Позафракційний',
            'information': 'Інформація',
            'email': 'someemail@test.com',
            'phone': '+3809903391212',
            'photo': mock_file
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
