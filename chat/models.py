from django.db import models
from django.contrib.auth import get_user_model
from account.models import Account


# Create your models here.
class Room(models.Model):
    room_id = models.AutoField(primary_key=True)
    first_user_id = models.ForeignKey(Account, related_name='user1', on_delete=models.CASCADE)
    second_user_id = models.ForeignKey(Account, related_name='user2', on_delete=models.CASCADE)

    def __str__(self):
        return "ID: " + str(self.room_id) + \
               " With: " + self.first_user_id.username + " + " + self.second_user_id.username


class Message(models.Model):
    # Chat message created by the user inside a ChatRoom (Foreign key)
    room_id = models.ForeignKey(Room, related_name='message', on_delete=models.CASCADE)
    sender_id = models.ForeignKey(Account, related_name='sender', on_delete=models.CASCADE)
    content = models.TextField(unique=False, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender_id.username + ": " + self.content

    def last_30_messages(self, message):
        return Message.objects.order_by('-timestamp').filter(room_id=message.room_id)

