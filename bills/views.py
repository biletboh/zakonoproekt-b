from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from rest_condition import Or

from bills.models import Bill
from bills.serializers import BillSerializer
from core.permissions import IsGetRequest


class BillViewSet(viewsets.ModelViewSet):
    """A viewset for viewing and editing bill instances."""

    permission_classes = [Or(IsAuthenticated, IsGetRequest)]
    serializer_class = BillSerializer
    queryset = Bill.objects.all()
