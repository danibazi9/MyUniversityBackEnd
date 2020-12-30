from rest_framework import serializers
from ..models import *


class ProfessorSerializer(serializers.ModelSerializer):
    free_times = serializers.StringRelatedField(format="%H:%M")
    research_axes = serializers.StringRelatedField(read_only=True)
    faculty = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Professor
        fields = '__all__'


class TimeSerializer(serializers.ModelSerializer):
    start_time = serializers.StringRelatedField(format="%H:%M")
    end_time = serializers.StringRelatedField(format="%H:%M")
    weekday = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Time
        fields = '__all__'


class ResearchAxisSerializer(serializers.ModelSerializer):
    faculty = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ResearchAxis
        fields = '__all__'
