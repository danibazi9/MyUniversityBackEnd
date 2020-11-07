from django.core.validators import MinLengthValidator
from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=40)
    email = models.EmailField(max_length=256, unique=True)
    student_id = models.IntegerField(unique=True)
    mobile_number = models.CharField(max_length=11, default="09100000000")
    password = models.CharField(max_length=20, validators=[MinLengthValidator(6)], blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name + " " + str(self.student_id)


class Contact(models.Model):
    user = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    friends =models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.user.last_name + " " + str(self.user.student_id)


class Message(models.Model):
    contact = models.ForeignKey(Contact, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.contact.user.first_name + " " + self.contact.user.last_name


class Chat(models.Model):
    participants = models.ManyToManyField(Contact, related_name='chats')
    messages = models.ManyToManyField(Message, blank=True)

    def last_10_messages(self):
        return self.messages.objects.order_by('-timestamp').all()[::-1]

    def __str__(self):
        return "{}".format(self.pk)
