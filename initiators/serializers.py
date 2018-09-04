from rest_framework import serializers

from initiators.models import Initiator


class InitiatorSerializer(serializers.HyperlinkedModelSerializer):
    """Serialize data for Initiator."""

    class Meta:
        model = Initiator
        fields = ('id', 'first_name', 'last_name', 'middle_name',
                  'convocation', 'party', 'faction', 'information', 'email',
                  'phone', 'photo', 'rada_id', 'url')
        extra_kwargs = {
            'url': {'view_name': 'initiators-detail'}
            }
