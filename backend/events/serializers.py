from rest_framework import serializers

from events.models import Event


class EventSerializer(serializers.ModelSerializer):
    """
    Event Serializer
    """
    count_participants = serializers.SerializerMethodField()
    attends = serializers.SerializerMethodField()
    created_by = serializers.SlugRelatedField('username', read_only=True)

    def get_attends(self, event):
        """
        Returns a boolean value that defines if the current user
        will attend this event
        :param event: Event instance
        :return: Boolean value if the user will assist to the event
        """
        account = self.context.get('request').user
        return event.has_participant(account=account)

    @staticmethod
    def get_count_participants(event):
        """
        Count the number of participants of the current event
        :param event: Event instance
        :return: Integer with the number of participants of the current event
        """
        return event.participants.count()

    class Meta:
        model = Event
        fields = (
            'id', 'title', 'description', 'date', 'created_by',
            'attends', 'count_participants'
        )
        read_only_fields = ['created_by']

    def create(self, validated_data):
        """
        Overrides event creation to set the owner of the object
        :param validated_data: Event validated data
        :return: Event instance
        """
        request = self.context.get('request')
        validated_data['created_by'] = request.user
        return super().create(validated_data)


class AttendEventSerializer(serializers.Serializer):
    """ Attend Event Serializer """
    attend = serializers.BooleanField()

    def validate_attend(self, attend):
        """
        Validate if the user will already attend the meeting
        :param attend: Boolean value if will attend the meeting
        :return: Boolean value with the attending attribute
        """
        event = self.context.get('event')
        account = self.context.get('request').user
        is_participant = event.has_participant(account=account)
        if attend and is_participant:
            raise serializers.ValidationError('You are already going to this event.')
        elif not attend and not is_participant:
            raise serializers.ValidationError('You have decided not going to this event.')
        return attend

    def save(self, **kwargs):
        """
        Create action when the user defines if will attend the meeting
        :return: None
        """
        event = self.context.get('event')
        account = self.context.get('request').user
        attend = self.validated_data.get('attend')
        if attend:
            account.attends.add(event)
        else:
            account.attends.remove(event)
