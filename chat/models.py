from django.db import models
from django.contrib.auth import get_user_model
from account.models import Account


# Create your models here.
class Contact(models.Model):
    user = models.OneToOneField(Account, related_name='friends', on_delete=models.CASCADE)
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.user.username + " " + str(self.user.student_id)


class Message(models.Model):
    # Chat message created by the user inside a ChatRoom (Foreign key)
    contact = models.ForeignKey(Contact, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField(unique=False, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.contact.user.username + ": " + self.content


class Chat(models.Model):
    title = models.CharField(max_length=30)
    user = models.ManyToManyField(Contact, related_name='chats')
    messages = models.ManyToManyField(Message, blank=True)

    def last_10_messages(self):
        return self.messages.objects.order_by('-timestamp').all()[:10]

    def __str__(self):
        return "ID: " + str(self.id) + " Title: " + self.title
