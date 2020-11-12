from django.contrib import admin
from BookBSE import models
# Register your models here.
admin.site.register(models.Faculty)
admin.site.register(models.Field)
admin.site.register(models.Book)
admin.site.register(models.Stock)
admin.site.register(models.Trade)
admin.site.register(models.Demand)