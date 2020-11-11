import json
import random

from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import *


def get_user(stuID):
    try:
        user_to_find = User.objects.get(student_id=stuID)
        return user_to_find
    except User.DoesNotExist:
        return None


# Create your views here.
class ChatList(APIView):
    def get(self, request):
        all_chats = Chat.objects.all()
        serializer = ChatSerializer(all_chats, many=True)
        return Response(serializer.data)

    # def post(self, request):


class ChatDetails(APIView):
    def get(self, request, stuID):
        user = get_user(stuID)
        if not user:
            return Response(f"User with student_id {stuID} Not Found!", status=status.HTTP_404_NOT_FOUND)

        try:
            contact = Contact.objects.get(user=user)
        except Contact.DoesNotExist:
            return Response(f"Contact with student_id {stuID} Not Found!", status=status.HTTP_404_NOT_FOUND)

        chats = contact.chats.all()
        serializer = ChatSerializer(chats, many=True)
        return serializer.data


#
#     def put(self, request, stuID):
#         user_to_edit = get_user(stuID)
#         if not user_to_edit:
#             return Response(f"User with student_id {stuID} Not Found!", status=status.HTTP_404_NOT_FOUND)
#         serializer = UserSerializer(user_to_edit, data=request.data)
#         if serializer.is_valid():
#             if 'email' in serializer.validated_data:
#                 if validate_email(serializer.validated_data.get('email')):
#                     if serializer.validated_data.get('email').endswith('.iust.ac.ir'):
#                         serializer.save()
#                         return Response(serializer.data, status=status.HTTP_201_CREATED)
#                     else:
#                         return Response(f"The email '{serializer['email'].value}' isn't the academical university email",
#                                         status=status.HTTP_406_NOT_ACCEPTABLE)
#                 else:
#                     return Response(f"The email '{serializer['email'].value}' doesn't exist",
#                                     status=status.HTTP_406_NOT_ACCEPTABLE)
#             else:
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, stuID):
#         user_to_delete = get_user(stuID)
#         if not user_to_delete:
#             return Response(f"User with student_id {stuID} Not Found!", status=status.HTTP_404_NOT_FOUND)
#         user_to_delete.delete()
#         return Response(f"The user with student_id {stuID} has deleted successfully!", status=status.HTTP_204_NO_CONTENT)


class ContactList(APIView):
    def get(self, request):
        all_contacts = Contact.objects.all()
        serializer = ContactSerializer(all_contacts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class ContactDetails(APIView):
#     def get(self, request, stuID):
#         user = get_user(stuID)
#         if not user:
#             return Response(f"User with student_id {stuID} Not Found!", status=status.HTTP_404_NOT_FOUND)
#         contact = get_object_or_404(Contact, user=user)
#         serializer = ChatSerializer(contact.chats().all())
#         return Response(serializer.data)
