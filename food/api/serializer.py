from rest_framework import serializers
from account.models import Account
from food.models import *


class FoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Food
        fields = '__all__'


class ServeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Serve
        fields = '__all__'
