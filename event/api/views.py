import base64
import datetime
import json

from django.core.files.base import ContentFile
from django.db.models import Q
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
            EventAuthorizedOrganizer.objects.get(user=self.request.user)
        except EventAuthorizedOrganizer.DoesNotExist:
            return Response("ERROR: You haven't access to add event!", status=status.HTTP_401_UNAUTHORIZED)

        try:
            organizer = Organization.objects.get(head_of_organization=self.request.user)
        except Organization.DoesNotExist:
            return Response("ERROR: There isn't any organization that you are the head of it!",
                            status=status.HTTP_404_NOT_FOUND)

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

    def put(self, arg):
        try:
            EventAuthorizedOrganizer.objects.get(user=self.request.user)
        except EventAuthorizedOrganizer.DoesNotExist:
            return Response("ERROR: You haven't access to edit event!", status=status.HTTP_401_UNAUTHORIZED)

        try:
            Organization.objects.get(head_of_organization=self.request.user)
        except Organization.DoesNotExist:
            return Response("ERROR: There isn't any organization that you are the head of it!",
                            status=status.HTTP_404_NOT_FOUND)

        event_id = self.request.query_params.get('event_id', None)
        if event_id is not None:
            try:
                event = Event.objects.get(event_id=event_id)
            except Event.DoesNotExist:
                return Response(f"event_id={event_id}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)

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

            my_serializer = EventSerializer(event)
            data = json.loads(json.dumps(my_serializer.data))
            data['organizer'] = data['organizer'].split(",    Head")[0]
            del data['verified']

            new_data = {'message': f"Event: event_id {event.event_id} has edited successfully!", 'data': data}
            return Response(new_data, status=status.HTTP_205_RESET_CONTENT)
        else:
            return Response("event_id: None, BAD REQUEST ", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, arg):
        try:
            EventAuthorizedOrganizer.objects.get(user=self.request.user)
        except EventAuthorizedOrganizer.DoesNotExist:
            return Response("ERROR: You haven't access to delete event!", status=status.HTTP_401_UNAUTHORIZED)

        try:
            Organization.objects.get(head_of_organization=self.request.user)
        except Organization.DoesNotExist:
            return Response("ERROR: There isn't any organization that you are the head of it!",
                            status=status.HTTP_404_NOT_FOUND)

        event_id = self.request.query_params.get('event_id', None)
        if event_id is not None:
            try:
                event_to_delete = Event.objects.get(event_id=event_id)

                start_time = event_to_delete.start_time
                end_time = event_to_delete.end_time

                event_start_time_datetime = datetime.datetime(year=start_time.year, month=start_time.month,
                                                              day=start_time.day, hour=start_time.hour,
                                                              minute=start_time.minute, second=start_time.second)

                event_end_time_datetime = datetime.datetime(year=end_time.year, month=end_time.month,
                                                            day=end_time.day, hour=end_time.hour,
                                                            minute=end_time.minute, second=end_time.second)

                if event_start_time_datetime.timestamp() < datetime.datetime.now().timestamp():
                    return Response(f"ERROR: the start_time of event is for the past!",
                                    status=status.HTTP_400_BAD_REQUEST)

                if event_end_time_datetime.timestamp() < datetime.datetime.now().timestamp():
                    return Response(f"ERROR: the end_time of event is for the past!",
                                    status=status.HTTP_400_BAD_REQUEST)
            except Event.DoesNotExist:
                return Response(f"event_id={event_id}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("event_id: None, BAD REQUEST ", status=status.HTTP_400_BAD_REQUEST)

        event_to_delete.delete()
        return Response(f"event_id: {event_id}, DELETED", status=status.HTTP_200_OK)


@permission_classes((IsAuthenticated,))
class UserEventsHistory(APIView):
    def get(self, args):
        try:
            EventAuthorizedOrganizer.objects.get(user=self.request.user)
        except EventAuthorizedOrganizer.DoesNotExist:
            return Response("ERROR: You haven't access to see history of events!", status=status.HTTP_401_UNAUTHORIZED)

        try:
            Organization.objects.get(head_of_organization=self.request.user)
        except Organization.DoesNotExist:
            return Response("ERROR: There isn't any organization that you are the head of it!",
                            status=status.HTTP_404_NOT_FOUND)

        events = Event.objects.filter(organizer__head_of_organization=self.request.user)
        serializer = EventSerializer(events, many=True)

        data = json.loads(json.dumps(serializer.data))
        for x in data:
            del x['organizer']

        return Response(data, status=status.HTTP_200_OK)


@permission_classes((IsAuthenticated,))
class AdminAuthAll(APIView):
    def get(self, args):
        try:
            culture_deputy = CultureDeputy.objects.get(user=self.request.user)
        except CultureDeputy.DoesNotExist:
            return Response("ERROR: You haven't been added as culture deputy of any faculty!",
                            status=status.HTTP_401_UNAUTHORIZED)

        if len(culture_deputy.organization_set.all()) == 0:
            return Response("Nothing! You haven't been added as culture deputy of any organization!",
                            status=status.HTTP_404_NOT_FOUND)

        search = self.request.query_params.get('search', None)
        state = self.request.query_params.get('state', None)

        if state is not None:
            if state == 'true':
                if search is None:
                    users_to_show = EventAuthorizedOrganizer.objects.filter(culture_deputy=culture_deputy). \
                        exclude(user_id=culture_deputy.user_id).exclude(is_admin=True)
                else:
                    users_to_show = EventAuthorizedOrganizer.objects.filter(Q(culture_deputy=culture_deputy),
                                                                            ~Q(user__user_id=culture_deputy.user_id),
                                                                            (Q(user__first_name__icontains=search) |
                                                                             Q(user__last_name__icontains=search) |
                                                                             Q(user__username__icontains=search)
                                                                             )).exclude(user__is_admin=True)
                serializer = EventAuthorizedOrganizerSerializer(users_to_show, many=True)

                data = json.loads(json.dumps(serializer.data))
                for x in data:
                    user = Account.objects.get(user_id=x['user'])
                    x['user_id'] = user.user_id
                    x['username'] = user.username
                    x['first_name'] = user.first_name
                    x['last_name'] = user.last_name
                    x['grant'] = True
                    del x['user']
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response("State: BAD REQUEST!", status=status.HTTP_400_BAD_REQUEST)
        else:
            if search is None:
                users_to_show = Account.objects.all().exclude(user_id=culture_deputy.user_id).exclude(is_admin=True)
            else:
                users_to_show = Account.objects.filter(~Q(user_id=culture_deputy.user_id),
                                                       ~Q(is_admin=True), (
                        Q(first_name__icontains=search) |
                        Q(last_name__icontains=search) |
                        Q(username__icontains=search)
                ))
            serializer = UserSerializer(users_to_show, many=True)

            data = json.loads(json.dumps(serializer.data))
            for x in data:
                try:
                    EventAuthorizedOrganizer.objects.get(user__username=x['username'])
                    x['grant'] = True
                except EventAuthorizedOrganizer.DoesNotExist:
                    x['grant'] = False

            return Response(data, status=status.HTTP_200_OK)


@permission_classes((IsAuthenticated,))
class AdminAuth(APIView):
    def get(self, args):
        try:
            culture_deputy = CultureDeputy.objects.get(user=self.request.user)
        except CultureDeputy.DoesNotExist:
            return Response("ERROR: You haven't been added as culture deputy of any faculty!",
                            status=status.HTTP_401_UNAUTHORIZED)

        if len(culture_deputy.organization_set.all()) == 0:
            return Response("Nothing! You haven't been added as culture deputy of any organization!",
                            status=status.HTTP_404_NOT_FOUND)

        user_id = self.request.query_params.get('user_id', None)

        if user_id is not None:
            try:
                my_user = Account.objects.get(user_id=user_id)
            except EventAuthorizedOrganizer.DoesNotExist:
                return Response(f"User with user_id {user_id} NOT FOUND!", status=status.HTTP_404_NOT_FOUND)

            try:
                user_to_show = EventAuthorizedOrganizer.objects.get(user=my_user)
                serializer = EventAuthorizedOrganizerSerializer(user_to_show)

                data = json.loads(json.dumps(serializer.data))
                user = Account.objects.get(username=data['user']['username'])
                data['user_id'] = user.user_id
                data['username'] = user.username
                data['first_name'] = user.first_name
                data['last_name'] = user.last_name
                data['grant'] = True
                del data['user']

                return Response(data, status=status.HTTP_200_OK)
            except EventAuthorizedOrganizer.DoesNotExist:
                user_to_show = Account.objects.get(user_id=user_id)
                data = {'user_id': user_to_show.user_id,
                        'username': user_to_show.username,
                        'first_name': user_to_show.first_name,
                        'last_name': user_to_show.last_name,
                        'grant': False
                        }

                return Response(data, status=status.HTTP_200_OK)
        else:
            return Response("user_id: None, BAD REQUEST!", status=status.HTTP_400_BAD_REQUEST)

    def post(self, args):
        try:
            culture_deputy = CultureDeputy.objects.get(user=self.request.user)
        except CultureDeputy.DoesNotExist:
            return Response("ERROR: You haven't been added as culture deputy of any faculty!",
                            status=status.HTTP_401_UNAUTHORIZED)

        if len(culture_deputy.organization_set.all()) == 0:
            return Response("Nothing! You haven't been added as culture deputy of any organization!",
                            status=status.HTTP_404_NOT_FOUND)

        request_body = json.loads(self.request.body)

        if 'user_id' not in request_body:
            return Response("user_id: None, BAD REQUEST!", status=status.HTTP_400_BAD_REQUEST)
        if 'grant' not in request_body:
            return Response("grant: None, BAD REQUEST!", status=status.HTTP_400_BAD_REQUEST)

        user_id = request_body['user_id']
        grant = request_body['grant']

        try:
            my_user = Account.objects.get(user_id=user_id)
        except Account.DoesNotExist:
            return Response(f"User with user_id {user_id} NOT FOUND!", status=status.HTTP_404_NOT_FOUND)

        if grant == 'true':
            user_to_search = EventAuthorizedOrganizer.objects.filter(user=my_user, culture_deputy=culture_deputy)
            if len(user_to_search) != 0:
                return Response(f"Redundant! User with user_id {my_user.user_id} has access to add events!",
                                status=status.HTTP_302_FOUND)
            else:
                EventAuthorizedOrganizer.objects.create(user=my_user, culture_deputy=culture_deputy)
                return Response("Successfully granted access to add events!", status=status.HTTP_200_OK)
        elif grant == 'false':
            user_to_search = EventAuthorizedOrganizer.objects.filter(user=my_user, culture_deputy=culture_deputy)
            if len(user_to_search) == 0:
                return Response(f"Redundant! User with user_id {my_user.user_id} hasn't access to add events!",
                                status=status.HTTP_302_FOUND)
            else:
                user_to_search.delete()
                return Response("Successfully refused access to add events!", status=status.HTTP_200_OK)
        else:
            return Response("grant: BAD REQUEST!", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_all_requests(request):
    try:
        culture_deputy = CultureDeputy.objects.get(user=request.user)
    except CultureDeputy.DoesNotExist:
        return Response("ERROR: You haven't been added as culture deputy of any faculty!",
                        status=status.HTTP_401_UNAUTHORIZED)

    if len(culture_deputy.organization_set.all()) == 0:
        return Response("Nothing! You haven't been added as culture deputy of any organization!",
                        status=status.HTTP_404_NOT_FOUND)

    search = request.query_params.get('search', None)
    state = request.query_params.get('state', None)

    if state is not None:
        if state == 'true':
            if search is None:
                events_to_show = Event.objects.filter(organizer__culture_deputy=culture_deputy, verified=True,
                                                      end_time__gt=datetime.datetime.now())
            else:
                events_to_show = Event.objects.filter(organizer__culture_deputy=culture_deputy, verified=True,
                                                      name__icontains=search, end_time__gt=datetime.datetime.now())
            serializer = EventSerializer(events_to_show, many=True)

            data = json.loads(json.dumps(serializer.data))
            for x in data:
                x['organizer'] = x['organizer'].split(",    Head")[0]
                del x['verified']
            return Response(data, status=status.HTTP_200_OK)
        elif state == "false":
            if search is None:
                events_to_show = Event.objects.filter(organizer__culture_deputy=culture_deputy, verified=False,
                                                      end_time__gt=datetime.datetime.now())
            else:
                events_to_show = Event.objects.filter(organizer__culture_deputy=culture_deputy, verified=False,
                                                      name__icontains=search, end_time__gt=datetime.datetime.now())
            serializer = EventSerializer(events_to_show, many=True)

            data = json.loads(json.dumps(serializer.data))
            for x in data:
                x['organizer'] = x['organizer'].split(",    Head")[0]
                del x['verified']
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response("State: BAD REQUEST!", status=status.HTTP_400_BAD_REQUEST)
    else:
        if search is None:
            events_to_show = Event.objects.filter(organizer__culture_deputy=culture_deputy,
                                                  end_time__gt=datetime.datetime.now())
        else:
            events_to_show = Event.objects.filter(organizer__culture_deputy=culture_deputy, name__icontains=search,
                                                  end_time__gt=datetime.datetime.now())

        serializer = EventSerializer(events_to_show, many=True)
        data = json.loads(json.dumps(serializer.data))
        for x in data:
            x['organizer'] = x['organizer'].split(",    Head")[0]
        return Response(data, status=status.HTTP_200_OK)


@permission_classes((IsAuthenticated,))
class Requests(APIView):
    def get(self, args):
        try:
            culture_deputy = CultureDeputy.objects.get(user=self.request.user)
        except CultureDeputy.DoesNotExist:
            return Response("ERROR: You haven't been added as culture deputy of any faculty!",
                            status=status.HTTP_401_UNAUTHORIZED)

        if len(culture_deputy.organization_set.all()) == 0:
            return Response("Nothing! You haven't been added as culture deputy of any organization!",
                            status=status.HTTP_404_NOT_FOUND)

        event_id = self.request.query_params.get('event_id', None)

        if event_id is not None:
            try:
                event_to_show = Event.objects.get(event_id=event_id)
            except Event.DoesNotExist:
                return Response(f"Event with event_id {event_id} NOT FOUND!", status=status.HTTP_404_NOT_FOUND)

            serializer = EventSerializer(event_to_show)
            data = json.loads(json.dumps(serializer.data))
            data['organizer'] = data['organizer'].split(",    Head")[0]

            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response("event_id: None, BAD REQUEST!", status=status.HTTP_400_BAD_REQUEST)

    def post(self, args):
        try:
            culture_deputy = CultureDeputy.objects.get(user=self.request.user)
        except CultureDeputy.DoesNotExist:
            return Response("ERROR: You haven't been added as culture deputy of any faculty!",
                            status=status.HTTP_401_UNAUTHORIZED)

        if len(culture_deputy.organization_set.all()) == 0:
            return Response("Nothing! You haven't been added as culture deputy of any organization!",
                            status=status.HTTP_404_NOT_FOUND)

        request_body = json.loads(self.request.body)

        if 'event_id' not in request_body:
            return Response("event_id: None, BAD REQUEST!", status=status.HTTP_400_BAD_REQUEST)
        if 'verified' not in request_body:
            return Response("verified: None, BAD REQUEST!", status=status.HTTP_400_BAD_REQUEST)

        event_id = request_body['event_id']
        verified = request_body['verified']

        try:
            my_event = Event.objects.get(event_id=event_id)
        except Event.DoesNotExist:
            return Response(f"Event with event_id {event_id} NOT FOUND!", status=status.HTTP_404_NOT_FOUND)

        if my_event.end_time.timestamp() < datetime.datetime.now().timestamp():
            return Response(f"ERROR: the event end_time is for the past!", status=status.HTTP_406_NOT_ACCEPTABLE)

        if verified == 'true':
            if my_event.verified:
                return Response(f"Redundant! Event with event_id {event_id} is verified!",
                                status=status.HTTP_302_FOUND)
            else:
                my_event.verified = True
                my_event.save()
                return Response("Event successfully verified!", status=status.HTTP_200_OK)
        elif verified == 'false':
            if not my_event.verified:
                return Response(f"Redundant! Event with event_id {event_id} isn't verified!",
                                status=status.HTTP_302_FOUND)
            else:
                my_event.verified = False
                my_event.save()
                return Response("Event successfully rejected!", status=status.HTTP_200_OK)
        else:
            return Response("verified: BAD REQUEST!", status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticated,))
class AdminRequestsHistory(APIView):
    def get(self, args):
        try:
            culture_deputy = CultureDeputy.objects.get(user=self.request.user)
        except CultureDeputy.DoesNotExist:
            return Response("ERROR: You haven't been added as culture deputy of any faculty!",
                            status=status.HTTP_401_UNAUTHORIZED)

        if len(culture_deputy.organization_set.all()) == 0:
            return Response("Nothing! You haven't been added as culture deputy of any organization!",
                            status=status.HTTP_404_NOT_FOUND)

        events = Event.objects.filter(culture_deputy=culture_deputy)
        serializer = EventSerializer(events, many=True)

        data = json.loads(json.dumps(serializer.data))
        for x in data:
            x['organizer'] = x['organizer'].split(",    Head")[0]

        return Response(data, status=status.HTTP_200_OK)
