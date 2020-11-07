from django.db import models
from MyUniversity.models import User


# Create your models here.
class ChatRoom(models.Model):
    title = models.CharField(max_length=255, unique=True, blank=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class ChatMessageManager(models.Manager):
    def by_room(self, room):
        qs = ChatMessage.objects.filter(room=room).order_by("-timestamp")
        return qs


class ChatMessage(models.Model):
    # Chat message created by the user inside a ChatRoom (Foreign key)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField(unique=False, blank=False)

    objects = ChatMessageManager()

    def __str__(self):
        return self.content
