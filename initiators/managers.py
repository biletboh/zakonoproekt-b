from django.db import models

from committees.models import Committee


class InitiatorManager(models.Manager):
    """Initiator model manager."""

    def create(self, committees_by_title=[], convocation_by_number=None,
               convocation_by_latin_number=None, **kwargs):
        """Save related models on create."""

        from initiators.models import Initiator

        initiator = Initiator(**kwargs)
        initiator.save()
        initiator = self.add_committees(initiator, committees_by_title)
        initiator = self.add_convocation_by_number(
            initiator, convocation_by_number)
        initiator = self.add_convocation_by_latin_number(
            initiator, convocation_by_latin_number)
        return initiator

    def add_committees(self, initiator, committee):
        """Add a committee to initiator object."""

        if committee:
            try:
                committee = Committee.objects.get(title=committee)
            except Committee.DoesNotExist:
                committee = Committee.objects.create(title=committee)

            initiator.committees.add(committee)
            initiator.save()

        return initiator

    def add_convocation_by_number(self, initiator, number):
        """Add a convocation to initiator object."""

        from initiators.models import Convocation

        if number:
            convocation = Convocation.objects.get(number=number)
            initiator.convocations.add(convocation)
            initiator.save()

        return initiator

    def add_convocation_by_latin_number(self, initiator, latin_number):
        """Add a convocation to initiator object."""

        from initiators.models import Convocation

        if latin_number:
            latin_number = self.format_latin_number(latin_number)
            convocation = Convocation.objects.get(latin_number=latin_number)
            initiator.convocations.add(convocation)
            initiator.save()

        return initiator

    def format_latin_number(self, latin_number):
        if 'скл.' in latin_number:
            latin_number = latin_number.replace('скл.', 'скликання')
        return latin_number
