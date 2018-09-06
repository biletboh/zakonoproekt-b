import os
import requests
import tablib
import time
import xlrd

from django.core.management.base import BaseCommand, CommandError

from committees.models import Committee


class Command(BaseCommand):

    help = 'Load committees from Rada departments xls'

    def download_xls(self, url, time_count=0):
        try:
            r = requests.get(url, allow_redirects=True, stream=True)
            return r
        except requests.exceptions.ConnectionError:
            time.sleep(1)
            time_count += 1
            if time_count < 10:
                return self.download_xls(url, time_count=time_count)
            else:
                message = f'Takes too long to connect to {url}'
                self.stdout.write(self.style.ERROR(message))
                return None

    def handle(self, *args, **options):
        url = 'http://data.rada.gov.ua/ogd/aut/staff/departments.xls'
        r = self.download_xls(url)

        if r:
            file_name = 'committees.xls'
            output = open(file_name, 'wb')
            output.write(r.content)

            workbook = xlrd.open_workbook('committees.xls')
            worksheet = workbook.sheet_by_index(0)

            for row in range(1, worksheet.nrows):
                department = worksheet.cell(row, 1).value
                if 'Комітет' in department:
                    c = Committee.objects.create(title=department)
                    print(c)

            committee_count = Committee.objects.count()

            os.remove(file_name)

            self.stdout.write(self.style.SUCCESS(
                f'Successfully loaded {committee_count} committees.'))
