from rest_framework import serializers

from bills.models import Bill, Passing, Document, AgendaQuestion, WorkOuts
from initiators.serializers import InitiatorSerializer


class PassingSerializer(serializers.ModelSerializer):
    """Serialize data for Committee."""

    class Meta:
        model = Passing
        fields = ('id', 'title', 'date')


class DocumentSerializer(serializers.ModelSerializer):
    """Serialize data for Document."""

    class Meta:
        model = Document
        fields = ('id', 'document_type', 'date', 'uri',
                  'document_file')


class AgendaSerializer(serializers.ModelSerializer):
    """Serialize data for AgendaQuestion."""

    class Meta:
        model = AgendaQuestion
        fields = ('id', 'bills', 'title', 'question_type', 'id_event',
                  'vote_for', 'vote_against', 'vote_abstain', 'not_voting',
                  'present', 'absent', 'total')


class WorkOutsSerializer(serializers.ModelSerializer):
    """Serialize data for WorkOuts."""

    class Meta:
        model = WorkOuts
        fields = ('id', 'title', 'date_passed', 'date_got')


class BillSerializer(serializers.ModelSerializer):
    """Serialize data for Committee."""

    chronology = PassingSerializer(many=True, required=False)
    authors = InitiatorSerializer(many=True, required=False)
    initiators = InitiatorSerializer(many=True, required=False)
    executives = InitiatorSerializer(many=True, required=False)
    main_executives = InitiatorSerializer(many=True, required=False)
    documents = DocumentSerializer(many=True, required=False)
    committees = WorkOutsSerializer(many=True, required=False)

    class Meta:
        model = Bill
        fields = ('id', 'title', 'bill_id', 'uri', 'number', 'convocation',
                  'session', 'rubric', 'subject', 'bill_type', 'phase',
                  'phase_date', 'registration_date', 'agenda_number',
                  'agenda_last_date', 'agenda_uri', 'bind_bills',
                  'alternatives', 'authors', 'initiators', 'executives',
                  'main_executives', 'chronology', 'documents', 'committees',
                  'url')
        extra_kwargs = {
            'url': {'view_name': 'bills-detail'}
            }

    def create(self, validated_data):
        bill = Bill.objects.create(
            title=validated_data['title'], bill_id=validated_data['bill_id'],
            number=validated_data['number'],
            convocation=validated_data['convocation'],
            session=validated_data['session'], rubric=validated_data['rubric'],
            subject=validated_data['subject'],
            bill_type=validated_data['bill_type'],
            phase=validated_data['phase'],
            phase_date=validated_data['phase_date'],
            uri=validated_data['uri'],
            registration_date=validated_data['registration_date'],
            agenda_uri=validated_data['agenda_uri'],
            agenda_number=validated_data['agenda_number'],
            agenda_last_date=validated_data['agenda_last_date'],
            chronology=validated_data.get('chronology', []),
            authors=validated_data.get('authors', []),
            initiators=validated_data.get('initiators', []),
            executives=validated_data.get('executives', []),
            main_executives=validated_data.get('main_executives', []),
            documents=validated_data.get('documents', []),
            committees=validated_data.get('committees', [])
            )
        return bill
