import datetime

from django.contrib import admin
from persiantools.jdatetime import JalaliDateTime

from BookBSE.models import *


class FacultyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    list_filter = ['name']

    class Meta:
        model = Faculty


admin.site.register(Faculty, FacultyAdmin)


class FieldAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'faculty']
    search_fields = ['name', 'faculty__name']
    list_filter = ['faculty']

    class Meta:
        model = Field


admin.site.register(Field, FieldAdmin)


class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'author', 'publisher', 'faculty', 'field']
    search_fields = ['name', 'author', 'publisher', 'faculty__name', 'field__name']
    list_filter = ['faculty', 'field']

    class Meta:
        model = Book


admin.site.register(Book, BookAdmin)


class StockAdmin(admin.ModelAdmin):
    list_display = ['id', 'book_name', 'book_author', 'book_publisher', 'edition', 'printno', 'price', 'seller']
    search_fields = ['book__name', 'edition', 'printno', 'price', 'seller']
    list_filter = ['book', 'seller']

    def book_name(self, obj):
        result = Book.objects.get(stock__id=obj.id)
        return result.name

    def book_author(self, obj):
        result = Book.objects.get(stock__id=obj.id)
        return result.author

    def book_publisher(self, obj):
        result = Book.objects.get(stock__id=obj.id)
        return result.publisher

    class Meta:
        model = Stock


admin.site.register(Stock, StockAdmin)


class TradeAdmin(admin.ModelAdmin):
    list_display = ['id', 'book_name', 'book_author', 'price', 'seller', 'buyer', 'get_trade', 'state']
    search_fields = ['book__name', 'seller__username', 'buyer__username']
    list_filter = ['seller', 'buyer', 'trade', 'state']

    def book_name(self, obj):
        result = Book.objects.get(trade__id=obj.id)
        return result.name

    def book_author(self, obj):
        result = Book.objects.get(stock__id=obj.id)
        return result.author

    def get_trade(self, obj):
        timestamp = datetime.datetime.timestamp(obj.trade)
        jalali_datetime = JalaliDateTime.fromtimestamp(timestamp)
        return jalali_datetime.strftime("%Y/%m/%d - %H:%M")

    class Meta:
        model = Trade


admin.site.register(Trade, TradeAdmin)


class DemandAdmin(admin.ModelAdmin):
    list_display = ['id', 'book_name', 'book_author', 'seller', 'client']
    search_fields = ['book__name', 'seller__first_name', 'seller__last_name', 'seller__username',
                     'client__first_name', 'client__last_name', 'client__username']
    list_filter = ['seller', 'client']

    def book_name(self, obj):
        result = Book.objects.get(trade__id=obj.id)
        return result.name

    def book_author(self, obj):
        result = Book.objects.get(stock__id=obj.id)
        return result.author

    class Meta:
        model = Demand


admin.site.register(Demand, DemandAdmin)


class ReportProblemAdmin(admin.ModelAdmin):
    list_display = ['id', 'accuser', 'accused', 'trade', 'text']
    search_fields = ['accuser__username', 'accused__username', 'trade', 'text']
    list_filter = ['accuser', 'accused', 'trade']

    class Meta:
        model = ReportProblem


admin.site.register(ReportProblem, ReportProblemAdmin)
