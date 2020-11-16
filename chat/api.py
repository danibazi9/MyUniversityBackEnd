import json
import random

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
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
def chat_properties_view(request):
    try:
        account = request.user
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        rooms = Room.objects.filter(first_user_id=account) | Room.objects.filter(second_user_id=account)
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST', ])
def create_room_view(request):
    try:
        account = request.user
    except Account.DoesNotExist:
        return Response("Authentication user Failed!", status=status.HTTP_404_NOT_FOUND)

    try:
        sender = Account.objects.get(user_id=request.POST['user_id'])
    except Account.DoesNotExist:
        return Response(f"The account with user_id {request.POST['user_id']} doesn't exist!",
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
