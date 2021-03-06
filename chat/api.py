import json

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from account.api.serializers import AccountPropertiesSerializer
from .serializer import *


def get_user(request):
    try:
        account = request.user
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return account


# Create your views here.
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def chat_properties_view(request):
    account = request.user

    if request.method == 'GET':
        rooms = Room.objects.filter(first_user_id=account) | Room.objects.filter(second_user_id=account)
        serializer = RoomSerializer(rooms, many=True)
        data = json.loads(json.dumps(serializer.data))
        for x in data:
            if account.user_id == x['second_user_id']:
                account_to_find = Account.objects.get(user_id=x['first_user_id'])
            else:
                account_to_find = Account.objects.get(user_id=x['second_user_id'])

            account_serializer = AccountPropertiesSerializer(account_to_find)
            account_data = json.loads(json.dumps(account_serializer.data))

            x['sender_image'] = account_data['image']

            first_account = Account.objects.get(user_id=x['first_user_id'])
            second_account = Account.objects.get(user_id=x['second_user_id'])

            x['first_user_id'] = account.first_name + " " + account.last_name

            if account.user_id == first_account.user_id:
                x['second_user_id'] = second_account.first_name + " " + second_account.last_name
            else:
                x['second_user_id'] = first_account.first_name + " " + first_account.last_name

            last_message = Message.objects.filter(room_id=x['room_id']).order_by('-timestamp')
            if len(last_message) != 0:
                message_serializer = MessageSerializer(last_message[0])
                message_data = json.loads(json.dumps(message_serializer.data))

                x['last_message'] = message_data['content']
                x['last_message_timestamp'] = message_data['timestamp']
            else:
                x['last_message'] = ""
                x['last_message_timestamp'] = ""

        return Response(data, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def create_room_view(request):
    account = request.user

    try:
        body = json.loads(request.body)
        sender = Account.objects.get(user_id=body['user_id'])
    except Account.DoesNotExist:
        return Response(f"The account with user_id {request.POST.get('user_id')} doesn't exist!",
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        room = Room.objects.filter(first_user_id=account, second_user_id=sender) | \
               Room.objects.filter(first_user_id=sender, second_user_id=account)
        if room:
            serializer = RoomSerializer(room, many=True)
            data = json.loads(json.dumps(serializer.data))
            return Response(data[0], status=status.HTTP_200_OK)
        else:
            room = Room.objects.create(first_user_id=account, second_user_id=sender)
            room.save()
            serializer = RoomSerializer(room)
            return Response(serializer.data, status=status.HTTP_200_OK)
