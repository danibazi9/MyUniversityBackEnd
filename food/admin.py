from django.contrib import admin
from . models import *


class FoodAdmin(admin.ModelAdmin):
    list_display = ['food_id', 'name', 'description', 'cost']
    search_fields = ['name', 'description']
    list_filter = ['food_id', 'name']

    class Meta:
        model = Food


admin.site.register(Food, FoodAdmin)


class ServeAdmin(admin.ModelAdmin):
    list_display = ['serve_id', 'food', 'seller', 'start_serve_time', 'end_serve_time',
                    'date', 'remaining_count', 'max_count']
    search_fields = ['food', 'seller']
    list_filter = ['food', 'seller', 'date']

    class Meta:
        model = Serve


admin.site.register(Serve, ServeAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'customer', 'total_price', 'ordered_items', 'last_update', 'done']
    search_fields = ['customer', 'ordered_items']
    list_filter = ['customer', 'done']

    class Meta:
        model = Order


admin.site.register(Order, OrderAdmin)


class TimeAdmin(admin.ModelAdmin):
    list_display = ['time_id', 'start_time', 'end_time']

    class Meta:
        model = Time


admin.site.register(Time, TimeAdmin)
