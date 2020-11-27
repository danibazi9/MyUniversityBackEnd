from django.db import models
from account.models import *


class Food(models.Model):
    food_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    image = models.ImageField(upload_to='images/', blank=True)
    cost = models.IntegerField(default=0)

    def __str__(self):
        return self.name + ", " + str(self.cost) + "R"


class Serve(models.Model):
    food_id = models.ForeignKey(Food, on_delete=models.CASCADE)
    seller_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    start_serve_time = models.TimeField()
    end_serve_time = models.TimeField()
    date = models.DateField(auto_now_add=True)
    remaining_count = models.IntegerField(default=0)

    def __str__(self):
        return "Seller: " + self.seller_id.username + ", Food: " + \
               self.food_id.name + ", Remaining count: " + str(self.remaining_count)

