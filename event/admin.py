from django.contrib import admin
from . models import *


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['organization_id', 'name', 'head_of_organization']
    search_fields = ['name', 'head_of_organization']
    list_filter = ['name', 'head_of_organization']

    class Meta:
        model = Organization


admin.site.register(Organization, OrganizationAdmin)


class EventAdmin(admin.ModelAdmin):
    list_display = ['event_id', 'name', 'organizer', 'start_time', 'end_time', 'hold_type']
    search_fields = ['name', 'organizer', 'description']
    list_filter = ['organizer', 'hold_type']

    class Meta:
        model = Event


admin.site.register(Event, EventAdmin)
