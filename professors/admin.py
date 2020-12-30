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
    list_display = ['research_axis_id', 'subject', 'faculty_name']
    search_fields = ['subject', 'faculty']
    list_filter = ['faculty']

    def faculty_name(self, obj):
        result = Faculty.objects.get(id=obj.id)
        return result.name

    class Meta:
        model = ResearchAxis


admin.site.register(ResearchAxis, ResearchAxisAdmin)


class ProfessorAdmin(admin.ModelAdmin):
    list_display = ['professor_id', 'first_name', 'last_name', 'faculty', 'academic_rank', 'email']
    search_fields = ['first_name', 'last_name', 'faculty', 'academic_rank', 'email', 'research_axes']
    list_filter = ['last_name', 'faculty', 'academic_rank', 'active']

    class Meta:
        model = Professor


admin.site.register(Professor, ProfessorAdmin)
