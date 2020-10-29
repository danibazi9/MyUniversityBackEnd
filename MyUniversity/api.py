import random

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from . serializers import *

from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from validate_email import validate_email


def get_user(stuID):
    try:
        user_to_find = User.objects.get(student_id=stuID)
        return user_to_find
    except User.DoesNotExist:
        return None


# Create your views here.
class UsersList(APIView):
    def get(self, request):
        all_users = User.objects.all()
        serializer = UserSerializer(all_users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            if validate_email(serializer.validated_data.get('email'), verify=True):
                if serializer.validated_data.get('email').endswith('.iust.ac.ir'):
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(f"The email '{serializer['email'].value}' isn't the academical university email",
                                    status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                return Response(f"The email '{serializer['email'].value}' doesn't exist",
                                status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersDetails(APIView):
    def get(self, request, stuID):
        user_to_show = get_user(stuID)
        if not user_to_show:
            return Response(f"User with student_id {stuID} Not Found!", status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user_to_show)
        return Response(serializer.data)

    def put(self, request, stuID):
        user_to_edit = get_user(stuID)
        if not user_to_edit:
            return Response(f"User with student_id {stuID} Not Found!", status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user_to_edit, data=request.data)
        if serializer.is_valid():
            if 'email' in serializer.validated_data:
                if validate_email(serializer.validated_data.get('email'), verify=True):
                    if serializer.validated_data.get('email').endswith('.iust.ac.ir'):
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    else:
                        return Response(f"The email '{serializer['email'].value}' isn't the academical university email",
                                        status=status.HTTP_406_NOT_ACCEPTABLE)
                else:
                    return Response(f"The email '{serializer['email'].value}' doesn't exist",
                                    status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)