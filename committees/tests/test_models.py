from django.test import TestCase

from committees.models import Committee
from core.mixins import BaseTestDataMixin


class CommitteeDataMixin(BaseTestDataMixin):
    """Mixin that adds Committee data."""

    def setUp(self):
        self.committee_data = {
            'title': ('Комітет Верховної Ради України з питань податкової та '
                      + 'митної політики'),
            'head': 'Тестун Тестенко',
            'description': 'Опис комітета',
            'number': 30,
            'website': 'committee.gov.ua',
            'secretary': 'Тестовий Секретар',
            'secretary_contacts': '(044) 255-37-21'
        }


class CommitteeModelTestCase(CommitteeDataMixin, TestCase):
    """Test the Committee model."""

    def test_can_create(self):
        """Test if the model can create a object."""

        old_count = Committee.objects.count()
        Committee.objects.create(**self.committee_data)
        new_count = Committee.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_str(self):
        """Test a string representation of the model."""

        test_object = Committee.objects.create(**self.committee_data)
        self.assertEqual(str(test_object), self.committee_data['title'])
