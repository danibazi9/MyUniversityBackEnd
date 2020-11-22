from django.contrib import admin
from BookBSE.models import *


# Register your models here.
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    list_filter = ['name']

    class Meta:
        model = Faculty


admin.site.register(Faculty, FacultyAdmin)


class FieldAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'faculty']
    search_fields = ['name', 'faculty']
    list_filter = ['name', 'faculty']

    class Meta:
        model = Field


admin.site.register(Field, FieldAdmin)


class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'author', 'publisher', 'faculty', 'field']
    search_fields = ['name', 'author', 'publisher', 'faculty', 'field']
    list_filter = ['faculty', 'field']

    class Meta:
        model = Book


admin.site.register(Book, BookAdmin)


class StockAdmin(admin.ModelAdmin):
    list_display = ['id', 'book_name', 'book_author', 'book_publisher', 'edition', 'printno', 'price', 'seller']
    search_fields = ['book', 'edition', 'printno', 'price', 'seller']
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
    list_display = ['id', 'book_name', 'book_author', 'price', 'seller', 'buyer', 'trade', 'state']
    search_fields = ['book', 'seller', 'buyer']
    list_filter = ['seller', 'buyer', 'trade', 'state']

    def book_name(self, obj):
        result = Book.objects.get(trade__id=obj.id)
        return result.name

    def book_author(self, obj):
        result = Book.objects.get(stock__id=obj.id)
        return result.author

    class Meta:
        model = Trade


admin.site.register(Trade, TradeAdmin)


class DemandAdmin(admin.ModelAdmin):
    list_display = ['id', 'book_name', 'book_author', 'seller', 'client']
    search_fields = ['book', 'seller', 'client']
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
    search_fields = ['accuser', 'accused', 'trade', 'text']
    list_filter = ['accuser', 'accused', 'trade']

    class Meta:
        model = ReportProblem


admin.site.register(ReportProblem, ReportProblemAdmin)
