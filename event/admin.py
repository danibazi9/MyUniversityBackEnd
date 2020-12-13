from django.contrib import admin
from . models import *


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['organization_id', 'name', 'head_of_organization']
    search_fields = ['name', 'head_of_organization']
    list_filter = ['name', 'head_of_organization']

    class Meta:
        model = Organization


admin.site.register(Organization, OrganizationAdmin)


class EventAuthorizedOrganizerAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name']
    search_fields = ['user']
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
    search_fields = ['user', 'faculty']
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
    list_display = ['event_id', 'name', 'organizer', 'start_time', 'end_time', 'verified']
    search_fields = ['name', 'organizer', 'description']
    list_filter = ['organizer', 'hold_type', 'verified']

    class Meta:
        model = Event


admin.site.register(Event, EventAdmin)
