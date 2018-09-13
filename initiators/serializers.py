from rest_framework import serializers

from initiators.models import Initiator, Convocation
from committees.serializers import CommitteeSerializer
from committees.models import Committee


class ConvocationSerializer(serializers.ModelSerializer):
    """Serialize data for Convocation."""

    class Meta:
        model = Convocation
        fields = ('number', 'latin_number')


class InitiatorSerializer(serializers.HyperlinkedModelSerializer):
    """Serialize data for Initiator."""

    convocations = ConvocationSerializer(many=True, read_only=True)
    committees = CommitteeSerializer(many=True, read_only=True)
    committee_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, required=False,
        queryset=Committee.objects.all(),
        source='committees')

    class Meta:
        model = Initiator
        fields = ('id', 'first_name', 'last_name', 'middle_name',
                  'convocations', 'party', 'faction', 'information', 'email',
                  'phone', 'photo', 'person_id', 'rada_id', 'url',
                  'committees', 'committee_ids')
        extra_kwargs = {
            'url': {'view_name': 'initiators-detail'}
            }
