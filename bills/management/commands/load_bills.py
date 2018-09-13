import requests

from django.core.management.base import BaseCommand

from bills.models import Bill
from bills.utils import BillParser
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
            parser = BillParser()
            for e in data:
                parsed_data = parser.parse(e)
                bill = Bill.objects.create(**parsed_data)
                yield bill

    def download_data(self, url):
        r = requests.get(
            'http://data.rada.gov.ua/ogd/zpr/skl8/bills-skl8.json')
        return r.status_code, r.json()
