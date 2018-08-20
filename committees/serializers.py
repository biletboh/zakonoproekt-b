from rest_framework import serializers

from committees.models import Committee


class CommitteeSerializer(serializers.ModelSerializer):
    """Serialize data for Committee."""

    class Meta:
        model = Committee
        fields = ('id', 'title', 'head', 'description', 'number', 'website',
                  'secretary', 'secretary_contacts')
