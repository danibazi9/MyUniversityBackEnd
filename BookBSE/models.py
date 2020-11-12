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

class Book(models.Model):
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=50)
    publisher = models.CharField(max_length=50)

    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'author', 'publisher')

    def __str__(self):
        return f"Name: {self.name}; Author: {self.author}; Publisher: {self.publisher}"