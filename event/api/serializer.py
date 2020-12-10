from rest_framework import serializers
from ..models import *


class EventSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    end_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    organizer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Event
        fields = '__all__'
