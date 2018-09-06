import os
import xlrd

from django.core.management.base import BaseCommand, CommandError

from committees.models import Committee
from core.mixins import FileDownloadCommandMixin


class Command(FileDownloadCommandMixin, BaseCommand):

    help = 'Load committees from Rada departments xls'

    def handle(self, *args, **options):
        url = 'http://data.rada.gov.ua/ogd/aut/staff/departments.xls'
        r = self.download_file(url)

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
