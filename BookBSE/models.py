from django.db import models

# Create your models here.
class Faculty(models.Model):
    name = models.CharField(max_length=125, unique=True)

    def __str__(self):
        return self.name

class Field(models.Model):
    name = models.CharField(max_length=125, unique=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return f"Faculty: {self.faculty.name}; Field: {self.name}"
