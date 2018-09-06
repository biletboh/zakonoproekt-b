import requests
import xlrd
import time


class BaseTestDataMixin:
    """Base mixin class to enable multiple inheritance for test data."""

    def setUp(self):
        pass


class FileDownloadCommandMixin:
    """Adds file download method to Command class."""

    def download_file(self, url, time_count=0):
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
                print(message)
                return None
