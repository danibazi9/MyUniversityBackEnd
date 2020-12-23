from django.contrib import admin
from . models import *


class TimeAdmin(admin.ModelAdmin):
    list_display = ['time_id', 'weekday', 'start_time', 'end_time']
    search_fields = ['weekday', 'start_time', 'end_time']
    list_filter = ['weekday']

    class Meta:
        model = Time


admin.site.register(Time, TimeAdmin)


class ResearchAxisAdmin(admin.ModelAdmin):
    list_display = ['researchaxis_id', 'subject']
    search_fields = ['subject']

    class Meta:
        model = Professor


admin.site.register(ResearchAxis, ResearchAxisAdmin)


class ProfessorAdmin(admin.ModelAdmin):
    list_display = ['professor_id', 'first_name', 'last_name', 'faculty', 'academic_rank', 'email']
    search_fields = ['first_name', 'last_name', 'faculty', 'academic_rank', 'email', 'research_axes']
    list_filter = ['last_name', 'faculty', 'academic_rank']

    class Meta:
        model = Professor


admin.site.register(Professor, ProfessorAdmin)
