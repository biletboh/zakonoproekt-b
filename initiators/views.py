from rest_framework import viewsets

from initiators.models import Initiator
from initiators.serializers import InitiatorSerializer


class InitiatorViewSet(viewsets.ModelViewSet):
    """A viewset for viewing and editing intiator instances."""

    serializer_class = InitiatorSerializer
    queryset = Initiator.objects.all()
