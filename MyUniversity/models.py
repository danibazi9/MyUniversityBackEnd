from django.core.validators import MinLengthValidator
from django.db import models


# Create your models here.
class University(models.Model):
    university_id = models.IntegerField(primary_key=True)
    university_name = models.CharField(max_length=30, unique=True)
    university_domain = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.university_name


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=256, unique=True)
    student_id = models.IntegerField()
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    mobile_number = models.BigIntegerField()
    password = models.CharField(max_length=20, validators=[MinLengthValidator(6)], blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name + " " + str(self.student_id)
