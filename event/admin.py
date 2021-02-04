import datetime

from django.contrib import admin
from persiantools.jdatetime import JalaliDateTime

from . models import *


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['organization_id', 'name', 'head_of_organization']
    search_fields = ['name', 'head_of_organization__first_name', 'head_of_organization__last_name',
                     'head_of_organization__username']
    list_filter = ['name', 'head_of_organization']

    class Meta:
        model = Organization


admin.site.register(Organization, OrganizationAdmin)


class EventAuthorizedOrganizerAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'culture_deputy']
    search_fields = ['user__first_name', 'user__last_name', 'user__username']
    list_filter = ['user']

    def username(self, obj):
        result = Account.objects.get(user_id=obj.user.user_id)
        return result.username

    def first_name(self, obj):
        result = Account.objects.get(user_id=obj.user.user_id)
        return result.first_name

    def last_name(self, obj):
        result = Account.objects.get(user_id=obj.user.user_id)
        return result.last_name

    class Meta:
        model = EventAuthorizedOrganizer


admin.site.register(EventAuthorizedOrganizer, EventAuthorizedOrganizerAdmin)


class CultureDeputyAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'faculty_name']
    search_fields = ['user__first_name', 'user__last_name', 'user__username', 'faculty__name']
    list_filter = ['user', 'faculty']

    def first_name(self, obj):
        result = Account.objects.get(user_id=obj.user.user_id)
        return result.first_name

    def last_name(self, obj):
        result = Account.objects.get(user_id=obj.user.user_id)
        return result.last_name

    def faculty_name(self, obj):
        result = Faculty.objects.get(id=obj.faculty.id)
        return result.name

    class Meta:
        model = CultureDeputy


admin.site.register(CultureDeputy, CultureDeputyAdmin)


class EventAdmin(admin.ModelAdmin):
    list_display = ['event_id', 'name', 'organizer', 'culture_deputy', 'get_start_time', 'get_end_time',
                    'verified', 'remaining_capacity', 'capacity']
    search_fields = ['name', 'organizer__name', 'description', 'culture_deputy__first_name',
                     'culture_deputy__last_name', 'culture_deputy__username']
    list_filter = ['organizer', 'hold_type', 'culture_deputy', 'verified']

    def get_start_time(self, obj):
        timestamp = datetime.datetime.timestamp(obj.start_time)
        jalali_datetime = JalaliDateTime.fromtimestamp(timestamp)
        return jalali_datetime.strftime("%Y/%m/%d - %H:%M")

    def get_end_time(self, obj):
        timestamp = datetime.datetime.timestamp(obj.end_time)
        jalali_datetime = JalaliDateTime.fromtimestamp(timestamp)
        return jalali_datetime.strftime("%Y/%m/%d - %H:%M")

    class Meta:
        model = Event


admin.site.register(Event, EventAdmin)


class RegisterEventAdmin(admin.ModelAdmin):
    list_display = ['registerevent_id', 'username', 'first_name', 'last_name', 'event_name']
    search_fields = ['event__name', 'registrant__first_name', 'registrant__last_name', 'registrant__username']
    list_filter = ['event', 'registrant']

    def username(self, obj):
        result = Account.objects.get(user_id=obj.registrant.user_id)
        return result.username

    def first_name(self, obj):
        result = Account.objects.get(user_id=obj.registrant.user_id)
        return result.first_name

    def last_name(self, obj):
        result = Account.objects.get(user_id=obj.registrant.user_id)
        return result.last_name

    def event_name(self, obj):
        result = Event.objects.get(event_id=obj.event.event_id)
        return result.name

    class Meta:
        model = RegisterEvent


admin.site.register(RegisterEvent, RegisterEventAdmin)
