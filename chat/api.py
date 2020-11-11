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

    def post(self, request):
        chat_serializer = ChatSerializer(data=request.data)
        if chat_serializer.is_valid():
            sender_stuID = request.POST['sender_student_id']
            receiver_stuID = request.POST['receiver_student_id']

            sender_user = get_user(sender_stuID)
            if not sender_user:
                return Response(f"User with student_id {sender_stuID} Not Found!", status=status.HTTP_404_NOT_FOUND)

            receiver_user = get_user(receiver_stuID)
            if not receiver_user:
                return Response(f"User with student_id {receiver_stuID} Not Found!", status=status.HTTP_404_NOT_FOUND)

            try:
                sender_contact = Contact.objects.get(user__student_id=sender_stuID)
            except Contact.DoesNotExist:
                sender_contact = Contact.objects.create(user=sender_user)
                sender_contact.save()

            try:
                receiver_contact = Contact.objects.get(user__student_id=receiver_stuID)
            except Contact.DoesNotExist:
                receiver_contact = Contact.objects.create(user=receiver_user)
                receiver_contact.save()

            sender_contact.friends.add(receiver_contact)

            try:
                new_chat = Chat.objects.get(title=request.POST['title'])
            except Chat.DoesNotExist:
                new_chat = Chat.objects.create(title=request.POST['title'])
            new_chat.user.add(sender_contact)
            new_chat.user.add(receiver_contact)

            return Response(f"Chatroom with id {new_chat.id} has successfully created "
                            f"between {sender_user.student_id} & {receiver_user.student_id}!", status=status.HTTP_201_CREATED)
        return Response(chat_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
