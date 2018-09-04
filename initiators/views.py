from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from rest_condition import Or

from initiators.models import Initiator
from initiators.serializers import InitiatorSerializer
from core.permissions import IsGetRequest


class InitiatorViewSet(viewsets.ModelViewSet):
    """A viewset for viewing and editing intiator instances."""

    permission_classes = [Or(IsAuthenticated, IsGetRequest)]
    serializer_class = InitiatorSerializer
    queryset = Initiator.objects.all()
