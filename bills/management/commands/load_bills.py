import os
import requests
import xlrd
from datetime import datetime, date

from django.core.management.base import BaseCommand, CommandError

from bills.models import Bill
from core.mixins import FileDownloadCommandMixin


class Command(FileDownloadCommandMixin, BaseCommand):

    help = 'Load committees from Rada departments xls'

    def handle(self, *args, **options):
        url = 'http://data.rada.gov.ua/ogd/aut/staff/departments.xls'

        bills_stream = self.bills_stream(url)
        for bill in bills_stream:
            print('New bill has been addeded: ', bill)

        bills_count = Bill.objects.count()
        self.stdout.write(self.style.SUCCESS(
                f'Successfully loaded {bills_count} committees.'))

    def bills_stream(self, url):
        status, data = self.download_data(url)
        if status == 200:
            for e in data:
                phase_date = datetime.strptime(e['currentPhase']['date'],
                                               '%d.%m.%Y').date()
                bill = Bill.objects.create(
                    title=e['title'], rada_id=e['id'], number=e['number'],
                    convocation=e['registrationConvocation'],
                    session=e['registrationSession'],
                    rubric=e['rubric'], subject=e['subject'],
                    bill_type=e['type'], phase=e['currentPhase']['title'],
                    phase_date=phase_date, uri=['uri'],
                    registration_date=e['registrationDate']
                    )
                agenda = e.get('agenda', None)
                if agenda:
                    bill.agenda_uri=e['agenda']['uri'],
                    bill.agenda_number=e['agenda']['number'],
                    bill.agenda_last_date=e['agenda']['date']
                    bill.save()
                yield bill

    def download_data(self, url):
        r = requests.get('http://data.rada.gov.ua/ogd/zpr/skl8/bills-skl8.json')
        return r.status_code, r.json()
