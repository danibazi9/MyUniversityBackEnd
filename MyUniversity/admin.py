from django.contrib import admin
from . import models

admin.site.register(models.User)
admin.site.register(models.Field)
admin.site.register(models.Faculty)
admin.site.register(models.Book)