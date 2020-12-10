import datetime
import json

from django.core.files.base import ContentFile
from django.utils.baseconv import base64
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from .serializer import *

from ..models import *


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_all_events(request):
    all_events = Event.objects.filter(end_time__gt=datetime.datetime.now(), verified=True)
    serializer = EventSerializer(all_events, many=True)
    data = json.loads(json.dumps(serializer.data))
    for x in data:
        x['organizer'] = x['organizer'].split(",    Head")[0]
        del x['verified']

    return Response(data, status=status.HTTP_200_OK)


@permission_classes((IsAuthenticated,))
class UserEvent(APIView):
    def get(self, args):
        event_id = self.request.query_params.get('event_id', None)
        if event_id is not None:
            try:
                event = Event.objects.get(event_id=event_id)
            except Event.DoesNotExist:
                return Response(f"Event with event_id {event_id} NOT FOUND!", status=status.HTTP_404_NOT_FOUND)

            serializer = EventSerializer(event)
            data = json.loads(json.dumps(serializer.data))
            data['organizer'] = data['organizer'].split(",    Head")[0]
            del data['verified']

            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response("Event_id: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)

    def post(self, args):

    def put(self, arg):
        event_id = self.request.query_params.get('event_id', None)
        if event_id is not None:
            try:
                event = Event.objects.get(event_id=event_id)
            except Event.DoesNotExist:
                return Response(f"event_id={event_id}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)

            serializer = EventSerializer(event, data=self.request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(f"{serializer.errors}, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("event_id: None, BAD REQUEST ", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, arg):
        event_id = self.request.query_params.get('event_id', None)
        if event_id is not None:
            try:
                event_to_delete = Event.objects.get(event_id=event_id)
            except Event.DoesNotExist:
                return Response(f"event_id={event_id}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("event_id: None, BAD REQUEST ", status=status.HTTP_400_BAD_REQUEST)

        event_to_delete.delete()
        return Response(f"event_id: {event_id}, DELETED", status=status.HTTP_200_OK)


@permission_classes((IsAuthenticated,))
class EventHistory(APIView):
    def get(self, args):
        events = Event.objects.filter(organizer__head_of_organization=self.request.user)
        serializer = EventSerializer(events, many=True)
        data = json.loads(json.dumps(serializer.data))

        return Response(data, status=status.HTTP_200_OK)
