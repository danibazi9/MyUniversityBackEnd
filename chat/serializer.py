from rest_framework import serializers

from chat.models import *


class RoomSerializer(serializers.ModelSerializer):
    # first_user_id = serializers.StringRelatedField(read_only=True)
    # second_user_id = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Room
        fields = ('room_id', 'first_user_id', 'second_user_id')


class MessageSerializer(serializers.ModelSerializer):
    sender_id = serializers.StringRelatedField(read_only=True)
    timestamp = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Message
        fields = ('room_id', 'sender_id', 'content', 'timestamp')
