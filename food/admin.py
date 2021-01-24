import datetime

from django.contrib import admin
from persiantools.jdatetime import JalaliDate, JalaliDateTime

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
                    'get_date', 'remaining_count', 'max_count']
    search_fields = ['food__name', 'seller__first_name', 'seller__last_name', 'seller__username']
    list_filter = ['food', 'seller', 'date']

    def get_date(self, obj):
        timestamp = datetime.datetime.timestamp(obj.date)
        jalali_datetime = JalaliDate.fromtimestamp(timestamp)
        return jalali_datetime.strftime("%Y/%m/%d")

    class Meta:
        model = Serve


admin.site.register(Serve, ServeAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'customer', 'total_price', 'ordered_items', 'get_last_update', 'done']
    search_fields = ['customer__first_name', 'customer__last_name', 'customer__username', 'ordered_items']
    list_filter = ['customer', 'done']

    def get_last_update(self, obj):
        timestamp = datetime.datetime.timestamp(obj.last_update)
        jalali_datetime = JalaliDateTime.fromtimestamp(timestamp)
        return jalali_datetime.strftime("%Y/%m/%d - %H:%M")

    class Meta:
        model = Order


admin.site.register(Order, OrderAdmin)


class TimeAdmin(admin.ModelAdmin):
    list_display = ['time_id', 'start_time', 'end_time']

    class Meta:
        model = Time


admin.site.register(Time, TimeAdmin)
