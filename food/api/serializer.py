from rest_framework import serializers
from food.models import *


class TimeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Time
        fields = '__all__'


class FoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Food
        fields = '__all__'


class AdminServeSerializer(serializers.ModelSerializer):
    food = FoodSerializer(read_only=True)

    class Meta:
        model = Serve
        fields = '__all__'


class UserAllServeSerializer(serializers.ModelSerializer):
    food = FoodSerializer(read_only=True)

    class Meta:
        model = Serve
        fields = ('serve_id', 'food', 'remaining_count', 'max_count', 'start_serve_time', 'end_serve_time')


class UserServeSerializer(serializers.ModelSerializer):
    food = FoodSerializer(read_only=True)

    class Meta:
        model = Serve
        fields = ('serve_id', 'food', 'remaining_count', 'max_count')


class OrderSerializer(serializers.ModelSerializer):
    last_update = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Order
        fields = ('order_id', 'customer', 'total_price', 'ordered_items', 'last_update', 'done')
