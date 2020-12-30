from rest_framework import serializers
from ..models import *


class ProfessorSerializer(serializers.ModelSerializer):
    faculty = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Professor
        fields = '__all__'


class TimeSerializer(serializers.ModelSerializer):
    start_time = serializers.StringRelatedField(read_only=True)
    end_time = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Time
        fields = '__all__'


class ResearchAxisSerializer(serializers.ModelSerializer):
    faculty = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ResearchAxis
        fields = '__all__'
