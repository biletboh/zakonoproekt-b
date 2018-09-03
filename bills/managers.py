from django.db import models

from committees.models import Committee


class BillManager(models.Manager):
    """Bill model manager."""

    def create(self, title, rada_id, number, convocation, session, rubric,
               subject, bill_type, phase, phase_date, uri='',
               registration_date=None, agenda_uri='', agenda_number=None,
               agenda_last_date=None, committee_date_passed=None,
               chronology=[], documents=[], committees=[], authors=[],
               initiators=[], executives=[], main_executives=[],
               **kwargs):
        """Save related models on create."""

        from bills.models import Bill

        bill = Bill(title=title, rada_id=rada_id, number=number,
                    convocation=convocation, session=session, rubric=rubric,
                    subject=subject, bill_type=bill_type, phase=phase,
                    phase_date=phase_date, uri=uri,
                    registration_date=registration_date,
                    agenda_number=agenda_number,
                    committee_date_passed=committee_date_passed)
        bill.save()
        bill = self.add_authors(bill, authors)
        bill = self.add_initiators(bill, initiators)
        bill = self.add_executives(bill, executives)
        bill = self.add_main_executives(bill, main_executives)
        bill = self.add_chronology(bill, chronology)
        bill = self.add_documents(bill, documents)
        bill = self.add_committees(bill, committees)
        return bill

    def add_authors(self, bill, authors):
        """Add authors to bill object."""

        if authors:
            bill.authors.add(*authors)
            bill.save()
        return bill

    def add_initiators(self, bill, initiators):
        """Add initiators to bill object."""

        if initiators:
            bill.initiators.add(*initiators)
            bill.save()
        return bill

    def add_executives(self, bill, executives):
        """Add executives to bill object."""

        if executives:
            bill.executives.add(*executives)
            bill.save()
        return bill

    def add_main_executives(self, bill, main_executives):
        """Add main executives to bill object."""

        if main_executives:
            bill.main_executives.add(*main_executives)
            bill.save()
        return bill

    def add_chronology(self, bill, chronology):
        """Add chronology to bill object."""

        from bills.models import Passing

        if chronology:
            for passing_data in chronology:
                passing = Passing.objects.create(**passing_data)
                bill.chronology.add(passing)
                bill.save()
        return bill

    def add_documents(self, bill, documents):
        """Add documents to bill object."""

        from bills.models import Document

        if documents:
            for document_data in documents:
                document_data['bill'] = bill
                Document.objects.create(**document_data)
        return bill

    def add_committees(self, bill, committees):
        """Add committees to bill object."""

        from bills.models import WorkOuts

        if committees:
            for workout_data in committees:
                title = workout_data['title']

                try:
                    committee = Committee.objects.get(title=title)
                except Committee.DoesNotExist:
                    committee = Committee.objects.create(title=title)

                workout_data['committee'] = committee
                workout_data['bill'] = bill
                WorkOuts.objects.create(**workout_data)

        return bill
