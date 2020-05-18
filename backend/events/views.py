""" Events Views """
import datetime

from django.db import models
from rest_framework import status, permissions, response, decorators, viewsets

from events.models import Event
from events.permissions import EventOwnerPermission
from events.serializers import EventSerializer, AttendEventSerializer


class EventViewSet(viewsets.ModelViewSet):
    """ Event ViewSet that defines Create-Read-Update-Delete of Events instances """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (EventOwnerPermission,)

    def get_queryset(self):
        """
        Update queryset to retrieve sorted events
        :return: Events queryset
        """
        queryset = super().get_queryset()
        today = datetime.datetime.today()
        return queryset.annotate(
            relevance=models.Case(
                models.When(date__gte=today, then=1),
                models.When(date__lt=today, then=2),
                output_field=models.IntegerField(),
            )).order_by('relevance', 'date')

    @decorators.action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated],
                       serializer_class=AttendEventSerializer)
    def attend(self, request, pk=None):
        """
        Define if the authenticated user will attend the event
        :param request:
        :param pk: Primary key of event
        :return: Response object empty
        """
        event = self.get_object()
        serializer = AttendEventSerializer(data=request.data, context={'event': event, 'request': request})
        if serializer.is_valid():
            serializer.save()
            return response.Response({}, status=status.HTTP_204_NO_CONTENT)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
