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
        try:
            authorized_organizer = EventAuthorizedOrganizer.objects.get(user=self.request.user)
        except EventAuthorizedOrganizer.DoesNotExist:
            return Response("ERROR: You haven't access to add event!", status=status.HTTP_401_UNAUTHORIZED)

        try:
            organizer = Organization.objects.get(head_of_organization=self.request.user)
        except Organization.DoesNotExist:
            return Response("ERROR: There isn't any organization that you are the head of it!",
                            status=status.HTTP_404_NOT_FOUND)

        serializer = EventSerializer(data=self.request.data)
        if serializer.is_valid():
            data = self.request.data

            file = ""
            if 'filename' in data and 'image' in data:
                filename = data['filename']
                file = ContentFile(base64.b64decode(data['image']), name=filename)

            description = ""
            if 'description' in data:
                description = data['description']

            capacity = 100
            if 'capacity' in data:
                capacity = data['capacity']

            cost = 0
            if 'cost' in data:
                cost = data['cost']

            event = Event(name=data['name'],
                          image=file,
                          organizer=organizer,
                          description=description,
                          start_time=datetime.datetime.strptime(data['start_time'], '%Y-%m-%d %H:%M:%S'),
                          end_time=datetime.datetime.strptime(data['end_time'], '%Y-%m-%d %H:%M:%S'),
                          hold_type=data['hold_type'],
                          location=data['location'],
                          cost=cost,
                          capacity=capacity,
                          remaining_capacity=capacity,
                          )

            event.save()
            new_data = {'event_id': event.event_id, 'message': "Event has added successfully!"}
            return Response(new_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
