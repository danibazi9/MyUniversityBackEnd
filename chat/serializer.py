from rest_framework import serializers
from MyUniversity.models import *


class ChatSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)

    class Meta:
        model = Chat
        fields = '__all__'
