import json
import os
import requests

from django.core.management.base import BaseCommand, CommandError

from initiators.models import Initiator
from core.mixins import FileDownloadCommandMixin


class Command(FileDownloadCommandMixin, BaseCommand):

    help = 'Load committees from Rada departments xls'

    def handle(self, *args, **options):
        url = 'http://data.rada.gov.ua/ogd/mps/skl8/mps08-data.json'
        r = requests.get(url)

        if r.status_code == 200:
            data = r.json()
            for e in data:
                if e['second_name']:
                    middle_name = e['second_name']
                i = Initiator.objects.create(
                        first_name=e['first_name'],
                        last_name=e['last_name'],
                        middle_name=middle_name,
                        convocation=e['convocation'],
                        party=e['party_name'],
                        information=e['anketa_data'],
                        rada_id=e['rada_id'])

                print(f'Initiator {i} is loaded.')

                i.save_photo(e['photo'])

            initiator_count = Initiator.objects.count()

            self.stdout.write(self.style.SUCCESS(
                f'Successfully loaded {initiator_count} initiators.'))

