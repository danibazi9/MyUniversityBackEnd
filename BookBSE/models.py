from django.db import models
from account.models import Account

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

class Stock(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    edition = models.IntegerField()
    printno = models.IntegerField()
    image = models.ImageField(upload_to='images/')
    price = models.IntegerField()

    seller = models.ForeignKey(Account, on_delete=models.CASCADE)
    upload = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('book', 'seller')

    def __str__(self):
        return f"Book: {self.book.__str__()}; Seller: {self.seller.__str__()}"

class Trade(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    edition = models.IntegerField()
    printno = models.IntegerField()
    image = models.ImageField(upload_to='images/')
    price = models.IntegerField()

    seller = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='seller')
    buyer = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='buyer')
    upload = models.DateTimeField()
    update = models.DateTimeField()
    reserve = models.DateTimeField(auto_now_add=True)
    trade = models.DateTimeField()
    state = models.BooleanField(default=False)

    class Meta:
        unique_together = ('book', 'seller', 'buyer')

    def __str__(self):
        return f"Book: {self.book.__str__()}; Seller: {self.seller.__str__()}; Buyer: {self.buyer.__str__()}"

