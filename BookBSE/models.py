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
        return self.name


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
    image = models.ImageField(upload_to='images/', blank=True)
    price = models.IntegerField()
    description = models.CharField(max_length=1024, null=True)

    seller = models.ForeignKey(Account, on_delete=models.CASCADE)
    upload = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    file = models.FileField(blank=True, null=True)
    # class Meta:
    #     unique_together = ('book', 'seller')

    def __str__(self):
        return f"Book: {self.book.__str__()}; Seller: {self.seller.__str__()}"


class Trade(models.Model):
    # book = models.ForeignKey(Book, on_delete=models.CASCADE)
    # edition = models.IntegerField()
    # printno = models.IntegerField()
    # image = models.ImageField(upload_to='images/', blank=True)
    # price = models.IntegerField()
    # description = models.CharField(max_length=1024, null=True)
    #
    # seller = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='seller')
    # buyer = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='buyer')
    # upload = models.DateTimeField()
    # update = models.DateTimeField()
    # reserve = models.DateTimeField(auto_now_add=True)
    # trade = models.DateTimeField(blank=True, null=True)
    # state = models.BooleanField(default=False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    image = models.URLField(null=True, blank=True)
    seller = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='seller')
    buyer = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='buyer')
    state = models.BooleanField(default=False)
    trade = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField()
    description = models.CharField(max_length=1024, null=True)

    class Meta:
        unique_together = ('book', 'seller', 'buyer')

    def __str__(self):
        return f"Book: {self.book.name}; Seller: {self.seller.username}; Buyer: {self.buyer.username}"


class Demand(models.Model):
    bookId = models.IntegerField(default=0)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    stock_id = models.IntegerField()
    seller = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='DemandSeller')
    client = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='DemandClient')
    imageUrl = models.URLField(blank=True, null=True)
    price = models.IntegerField()
    description = models.TextField(blank=True)
    # stockId = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('book', 'seller', 'client')

    def __str__(self):
        return f"Book: {self.book.name}; Seller: {self.seller.username}; Client: {self.client.username}"


class ReportProblem(models.Model):
    accuser = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='accuser')
    accused = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='accused')
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE)
    text = models.CharField(max_length=1024)

    # class Meta:
    #     unique_together = ('accuser', 'accused', 'trade')

    def __str__(self):
        return f"Accuser: {self.accuser.username}, Accused: {self.accused.username}, Trade: {self.trade.book.name}"
