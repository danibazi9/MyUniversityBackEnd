from django.core.validators import MinLengthValidator
from django.db import models


# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=256, unique=True)
    student_id = models.IntegerField()
    university = models.CharField(max_length=20)
    password = models.CharField(max_length=20, validators=[MinLengthValidator(6)])

    def __str__(self):
        return self.first_name + " " + self.last_name
