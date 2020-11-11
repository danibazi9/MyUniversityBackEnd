from django.db.models.functions import datetime
from rest_framework import serializers

from MyUniversity.serializer import UserSerializer
from chat.models import *
from MyUniversity.models import *


class ContactSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    friends = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Contact
        fields = ('user', 'friends')


class MessageSerializer(serializers.ModelSerializer):
    contact = serializers.StringRelatedField(read_only=True)
    timestamp = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Message
        fields = ('contact', 'content', 'timestamp')


class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(read_only=True, many=True)

    class Meta:
        model = Chat
        fields = ('title', 'messages')
