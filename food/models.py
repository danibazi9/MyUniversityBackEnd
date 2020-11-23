from django.db import models
from account.models import *


class Food(models.Model):
    food_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    image = models.ImageField(upload_to='images/', blank=True)
    cost = models.IntegerField()


class Serve(models.Model):
    food_id = models.ForeignKey(Food, on_delete=models.CASCADE)
    seller_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    time = models.TimeField()
    date = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField()
