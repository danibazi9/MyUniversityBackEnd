from django.contrib import admin
from . models import *


class FoodAdmin(admin.ModelAdmin):
    list_display = ['food_id', 'name', 'description', 'cost']
    search_fields = ['food_id', 'name', 'description']
    list_filter = ['food_id', 'name']

    class Meta:
        model = Food


admin.site.register(Food, FoodAdmin)


class ServeAdmin(admin.ModelAdmin):
    list_display = ['food_id', 'seller_id', 'time', 'date', 'count']
    search_fields = ['food_id', 'seller_id', 'time']
    list_filter = ['food_id', 'seller_id', 'time']

    class Meta:
        model = Serve


admin.site.register(Serve, ServeAdmin)
