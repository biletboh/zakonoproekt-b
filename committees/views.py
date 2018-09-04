from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from rest_condition import Or

from committees.models import Committee
from committees.serializers import CommitteeSerializer
from core.permissions import IsGetRequest


class CommitteeViewSet(viewsets.ModelViewSet):
    """A viewset for viewing and editing committee instances."""

    permission_classes = [Or(IsAuthenticated, IsGetRequest)]
    serializer_class = CommitteeSerializer
    queryset = Committee.objects.all()
