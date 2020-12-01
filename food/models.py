from django.db import models
from account.models import *
from django.utils import timezone


class Food(models.Model):
    food_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    image = models.ImageField(upload_to='food/images/', blank=True)
    cost = models.IntegerField(default=0)

    def __str__(self):
        return self.name + ", " + str(self.cost) + "R"


class Serve(models.Model):
    serve_id = models.AutoField(primary_key=True)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    seller = models.ForeignKey(Account, on_delete=models.CASCADE)
    start_serve_time = models.TimeField()
    end_serve_time = models.TimeField()
    date = models.DateField(default=timezone.now)
    remaining_count = models.IntegerField()
    max_count = models.IntegerField()

    class Meta:
        unique_together = ('food', 'seller', 'start_serve_time', 'end_serve_time', 'date')

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


class Time(models.Model):
    time_id = models.AutoField(primary_key=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return 'start_time: ' + str(self.start_time) + ', end_time: ' + str(self.end_time)
