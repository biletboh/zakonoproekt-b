from rest_framework import serializers

from bills.models import Bill, Passing, Document, AgendaQuestion, WorkOuts


class PassingSerializer(serializers.ModelSerializer):
    """Serialize data for Committee."""

    class Meta:
        model = Passing
        fields = ('id', 'title', 'date')


class DocumentSerializer(serializers.ModelSerializer):
    """Serialize data for Document."""

    class Meta:
        model = Document
        fields = ('id', 'bill', 'document_type', 'date', 'uri',
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
        fields = ('id', 'title', 'date_passed', 'date_got', 'bill',
                  'committee')


class BillSerializer(serializers.ModelSerializer):
    """Serialize data for Committee."""

    chronology = PassingSerializer(many=True, required=False)
    committees = WorkOutsSerializer(many=True, required=False)
    documents = DocumentSerializer(many=True, required=False)

    class Meta:
        model = Bill
        fields = ('id', 'title', 'rada_id', 'uri', 'number', 'convocation',
                  'session', 'rubric', 'subject', 'bill_type', 'phase',
                  'phase_date', 'registration_date', 'agenda_number',
                  'agenda_last_date', 'agenda_uri', 'committee_date_passed',
                  'bind_bills', 'alternatives', 'authors', 'executives',
                  'main_executives', 'chronology', 'committees', 'documents')

    def create(self, validated_data):
        bill = Bill.objects.create(validated_data)
        return bill
