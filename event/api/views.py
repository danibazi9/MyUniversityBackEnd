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

            start_time = datetime.datetime.strptime(data['start_time'], '%Y-%m-%d %H:%M:%S')
            start_time_datetime = datetime.datetime(year=start_time.year, month=start_time.month,
                                                    day=start_time.day, hour=start_time.hour,
                                                    minute=start_time.minute, second=start_time.second)

            end_time = datetime.datetime.strptime(data['end_time'], '%Y-%m-%d %H:%M:%S')
            end_time_datetime = datetime.datetime(year=end_time.year, month=end_time.month,
                                                  day=end_time.day, hour=end_time.hour,
                                                  minute=end_time.minute, second=end_time.second)

            if start_time_datetime.timestamp() < datetime.datetime.now().timestamp():
                return Response(f"ERROR: the start_time of event is for the past!", status=status.HTTP_400_BAD_REQUEST)

            if end_time_datetime.timestamp() < datetime.datetime.now().timestamp():
                return Response(f"ERROR: the end_time of event is for the past!", status=status.HTTP_400_BAD_REQUEST)

            if start_time_datetime.timestamp() > end_time_datetime.timestamp():
                return Response(f"ERROR: start_time is larger than end_time!", status=status.HTTP_400_BAD_REQUEST)

            if end_time_datetime.timestamp() - start_time_datetime.timestamp() < 1800:
                return Response(f"ERROR: The whole time of any event can't be less than 30 minutes!",
                                status=status.HTTP_400_BAD_REQUEST)

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
                          start_time=start_time,
                          end_time=end_time,
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
        try:
            authorized_organizer = EventAuthorizedOrganizer.objects.get(user=self.request.user)
        except EventAuthorizedOrganizer.DoesNotExist:
            return Response("ERROR: You haven't access to edit event!", status=status.HTTP_401_UNAUTHORIZED)

        try:
            organizer = Organization.objects.get(head_of_organization=self.request.user)
        except Organization.DoesNotExist:
            return Response("ERROR: There isn't any organization that you are the head of it!",
                            status=status.HTTP_404_NOT_FOUND)

        event_id = self.request.query_params.get('event_id', None)
        if event_id is not None:
            try:
                event = Event.objects.get(event_id=event_id)
            except Event.DoesNotExist:
                return Response(f"event_id={event_id}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)

            serializer = EventSerializer(event, data=self.request.data)
            if serializer.is_valid():
                data = self.request.data

                start_time = datetime.datetime.strptime(data['start_time'], '%Y-%m-%d %H:%M:%S')
                start_time_datetime = datetime.datetime(year=start_time.year, month=start_time.month,
                                                        day=start_time.day, hour=start_time.hour,
                                                        minute=start_time.minute, second=start_time.second)

                end_time = datetime.datetime.strptime(data['end_time'], '%Y-%m-%d %H:%M:%S')
                end_time_datetime = datetime.datetime(year=end_time.year, month=end_time.month,
                                                      day=end_time.day, hour=end_time.hour,
                                                      minute=end_time.minute, second=end_time.second)

                if start_time_datetime.timestamp() < datetime.datetime.now().timestamp():
                    return Response(f"ERROR: the start_time of event is for the past!",
                                    status=status.HTTP_400_BAD_REQUEST)

                if end_time_datetime.timestamp() < datetime.datetime.now().timestamp():
                    return Response(f"ERROR: the end_time of event is for the past!",
                                    status=status.HTTP_400_BAD_REQUEST)

                if start_time_datetime.timestamp() > end_time_datetime.timestamp():
                    return Response(f"ERROR: start_time is larger than end_time!", status=status.HTTP_400_BAD_REQUEST)

                if end_time_datetime.timestamp() - start_time_datetime.timestamp() < 1800:
                    return Response(f"ERROR: The whole time of any event can't be less than 30 minutes!",
                                    status=status.HTTP_400_BAD_REQUEST)

                file = ""
                if 'filename' in data and 'image' in data:
                    filename = data['filename']
                    file = ContentFile(base64.b64decode(data['image']), name=filename)

                description = ""
                if 'description' in data:
                    description = data['description']

                capacity = 100
                if 'capacity' in data:
                    capacity = int(data['capacity'])

                if capacity < event.remaining_capacity:
                    return Response(f"ERROR: You can't reduce the capacity of the event, "
                                    f"{event.remaining_capacity} people have registered to event!")

                cost = 0
                if 'cost' in data:
                    cost = data['cost']

                event.name = data['name']
                event.image = file
                event.description = description
                event.start_time = start_time
                event.end_time = end_time
                event.hold_type = data['hold_type']
                event.location = data['location']
                event.cost = cost
                event.remaining_capacity += (capacity - event.capacity)
                event.capacity = capacity

                event.save()

                mySerializer = EventSerializer(event)
                data = json.loads(json.dumps(mySerializer.data))
                data['organizer'] = data['organizer'].split(",    Head")[0]
                del data['verified']

                new_data = {'message': f"Event: event_id {event.event_id} has edited successfully!",
                            'data': data}

                return Response(new_data, status=status.HTTP_205_RESET_CONTENT)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
