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
    serve_id = models.AutoField(primary_key=True)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    seller = models.ForeignKey(Account, on_delete=models.CASCADE)
    start_serve_time = models.TimeField()
    end_serve_time = models.TimeField()
    date = models.DateField(auto_now_add=True)
    remaining_count = models.IntegerField()
    max_count = models.IntegerField()

    def __str__(self):
        return "Seller: " + self.seller.username + ", Food: " + \
               self.food.name + ", Remaining count: " + str(self.remaining_count)


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Account, on_delete=models.CASCADE)
    total_price = models.FloatField(default=0)
    ordered_items = models.CharField(max_length=300)
    last_update = models.DateTimeField(auto_now=True)
    done = models.BooleanField(default=False)

    def __str__(self):
        return "Customer: " + self.customer.username + \
               ", Total: " + str(self.total_price) + "R, Ordered: " + self.ordered_items
