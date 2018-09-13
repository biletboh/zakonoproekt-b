from django.db import models

from committees.models import Committee
from initiators.models import Initiator


class BillManager(models.Manager):
    """Bill model manager."""

    def create(self, title, bill_id, number, convocation, session, rubric,
               subject, bill_type, phase, phase_date, uri='',
               registration_date=None, agenda_uri='', agenda_number=None,
               agenda_last_date=None, agenda=None, chronology=[],
               documents=[], committees=[], authors=[],
               initiators=[], executives=[], main_executives=[],
               alternatives=[], bind_bills=[], **kwargs):
        """Save related models on create."""

        from bills.models import Bill

        bill = Bill(title=title, bill_id=bill_id, number=number,
                    convocation=convocation, session=session, rubric=rubric,
                    subject=subject, bill_type=bill_type, phase=phase,
                    phase_date=phase_date, uri=uri,
                    registration_date=registration_date,
                    agenda_number=agenda_number,
                    agenda_uri=agenda_uri,
                    agenda_last_date=agenda_last_date)
        bill.save()
        bill = self.add_agenda(bill, agenda)
        bill = self.add_authors(bill, authors)
        bill = self.add_initiators(bill, initiators)
        bill = self.add_executives(bill, executives)
        bill = self.add_main_executives(bill, main_executives)
        bill = self.add_chronology(bill, chronology)
        bill = self.add_documents(bill, documents)
        bill = self.add_committees(bill, committees)
        bill = self.add_bill_alternatives(bill, alternatives)
        bill = self.add_bind_bills(bill, bind_bills)
        return bill

    def add_agenda(self, bill, agenda):
        """Add agenda to a bill object."""

        if agenda:
            bill.agenda_uri = agenda['uri'],
            bill.agenda_number = agenda['number'],
            bill.agenda_last_date = agenda['date']
            bill.save()
        return bill

    def add_authors(self, bill, authors):
        """Add authors to a bill object."""

        if authors:
            for author in authors:
                person_id = author['person_id']

                try:
                    author = Initiator.objects.get(person_id=person_id)
                except Initiator.DoesNotExist:
                    author = Initiator.objects.create(**author)

                bill.authors.add(author)
            bill.save()
        return bill

    def add_initiators(self, bill, initiators):
        """Add initiators to a bill object."""

        if initiators:
            for initiator in initiators:
                person_id = initiator['person_id']

                try:
                    initiator = Initiator.objects.get(person_id=person_id)
                except Initiator.DoesNotExist:
                    initiator = Initiator.objects.create(**initiator)

                bill.initiators.add(initiator)
            bill.save()

        return bill

    def add_executives(self, bill, executives):
        """Add executives to a bill object."""

        if executives:
            for executive in executives:
                person_id = executive['person_id']

                try:
                    executive = Initiator.objects.get(person_id=person_id)
                except Initiator.DoesNotExist:
                    executive = Initiator.objects.create(**executive)

                bill.executives.add(executive)
            bill.save()

        return bill

    def add_main_executives(self, bill, main_executives):
        """Add main executives to a bill object."""

        if main_executives:
            for executive in main_executives:
                person_id = executive['person_id']

                try:
                    executive = Initiator.objects.get(person_id=person_id)
                except Initiator.DoesNotExist:
                    executive = Initiator.objects.create(**executive)

                bill.main_executives.add(executive)
            bill.save()

        return bill

    def add_chronology(self, bill, chronology):
        """Add chronology to a bill object."""

        from bills.models import Passing

        if chronology:
            for passing_data in chronology:
                passing = Passing.objects.create(**passing_data)
                bill.chronology.add(passing)
                bill.save()
        return bill

    def add_documents(self, bill, documents):
        """Add documents to a bill object."""

        from bills.models import Document

        if documents:
            for document_data in documents:
                document_data['bill'] = bill
                Document.objects.create(**document_data)
        return bill

    def add_committees(self, bill, committees):
        """Add committees to a bill object."""

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

                # check if an object exists to avoid dublicates
                if not WorkOuts.objects.filter(**workout_data).exists():
                    WorkOuts.objects.create(**workout_data)

        return bill

    def add_bill_alternatives(self, bill, bill_ids):
        """Add related alternatives to a bill object."""

        from bills.models import Bill

        if bill_ids:
            for bill_id in bill_ids:
                if Bill.objects.filter(**bill_id).exists():
                    related_bill = Bill.objects.get(**bill_id)
                    bill.alternatives.add(related_bill)
                    bill.save()
        return bill

    def add_bind_bills(self, bill, bill_ids):
        """Add related bind bills to a bill object."""

        from bills.models import Bill

        if bill_ids:
            for bill_id in bill_ids:
                if Bill.objects.filter(**bill_id).exists():
                    related_bill = Bill.objects.get(**bill_id)
                    bill.bind_bills.add(related_bill)
                    bill.save()
        return bill
