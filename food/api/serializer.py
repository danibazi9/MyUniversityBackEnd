from rest_framework import serializers
from account.models import Account
from food.models import *


class FoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Food
        fields = '__all__'


class AdminAllServeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Serve
        fields = '__all__'


class AdminServeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class UserAllServeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Serve
        fields = ('start_serve_time', 'end_serve_time', 'remaining_count')


class UserServeSerializer(serializers.ModelSerializer):
    food = FoodSerializer(read_only=True)

    class Meta:
        model = Serve
        fields = ('serve_id', 'food', 'remaining_count')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
