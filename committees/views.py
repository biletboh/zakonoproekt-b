from rest_framework import viewsets

from committees.models import Committee
from committees.serializers import CommitteeSerializer


class CommitteeViewSet(viewsets.ModelViewSet):
    """A viewset for viewing and editing committee instances."""

    serializer_class = CommitteeSerializer
    queryset = Committee.objects.all()
