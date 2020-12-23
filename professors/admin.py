from django.contrib import admin
from . models import *


class ProfessorAdmin(admin.ModelAdmin):
    list_display = ['professor_id', 'first_name', 'last_name', 'faculty', 'academic_rank', 'email']
    search_fields = ['first_name', 'last_name', 'faculty', 'academic_rank', 'email', 'research_axes']
    list_filter = ['last_name', 'faculty', 'academic_rank']

    class Meta:
        model = Professor


admin.site.register(Professor, ProfessorAdmin)
