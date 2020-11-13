from django.contrib import admin
from django.core.paginator import Paginator
from django.core.cache import cache
from django.db import models

from chat.models import *
# Register your models here.


class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['title', 'id']
    search_fields = ['title', 'user', 'id']
    list_filter = ['title', 'id']

    class Meta:
        model = Chat


admin.site.register(Chat, ChatRoomAdmin)


class CachingPaginator(Paginator):
    def _get_count(self):

        if not hasattr(self, "_count"):
            self._count = None

        if self._count is None:
            try:
                key = "adm:{0}:count".format(hash(self.object_list.query.__str__()))
                self._count = cache.get(key, -1)
                if self._count == -1:
                    self._count = super().count
                    cache.set(key, self._count, 3600)

            except:
                self._count = len(self.object_list)
        return self._count

    count = property(_get_count)


class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['contact', 'content', 'timestamp']
    list_filter = ['contact', 'timestamp']
    search_fields = ['contact__friends', 'content']

    show_full_result_count = False
    paginator = CachingPaginator

    class Meta:
        model = Message


admin.site.register(Message, ChatMessageAdmin)


class ContactAdmin(admin.ModelAdmin):
    list_display = ['user']
    list_filter = ['user']
    search_fields = ['user']

    class Meta:
        model = Contact


admin.site.register(Contact, ContactAdmin)
