from rest_framework import viewsets

from bills.models import Bill
from bills.serializers import BillSerializer


class BillViewSet(viewsets.ModelViewSet):
    """A viewset for viewing and editing bill instances."""

    serializer_class = BillSerializer
    queryset = Bill.objects.all()
