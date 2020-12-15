from rest_framework import serializers
from ..models import *


class EventSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    end_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    organizer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Event
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('username', 'first_name', 'last_name')


class EventAuthorizedOrganizerSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventAuthorizedOrganizer
        fields = ('user',)
