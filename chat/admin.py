import datetime

from django.contrib import admin
from django.core.paginator import Paginator
from django.core.cache import cache
from persiantools.jdatetime import JalaliDateTime

from chat.models import *


class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_id', 'first_user_id', 'second_user_id']
    search_fields = ['room_id', 'first_user_id__username', 'second_user_id__username']
    list_filter = ['room_id', 'first_user_id__username', 'second_user_id__username']

    class Meta:
        model = Room


admin.site.register(Room, RoomAdmin)


class CachingPaginator(Paginator):
    def _get_count(self):

        if not hasattr(self, "_count"):
            self._count = None

        if self._count is None:
            try:
                key = "adm:{0}:count".format(hash(self.object_list.query.__str__()))
                self._count = Account.objects.get(key, -1)
                if self._count == -1:
                    self._count = super().count
                    cache.set(key, self._count, 3600)

            except:
                self._count = len(self.object_list)
        return self._count

    count = property(_get_count)


class MessageAdmin(admin.ModelAdmin):
    list_display = ['room_id', 'sender_id', 'content', 'get_timestamp']
    list_filter = ['room_id', 'sender_id__username', 'timestamp']
    search_fields = ['room_id', 'sender_id__username', 'timestamp']

    show_full_result_count = False
    paginator = CachingPaginator

    def get_timestamp(self, obj):
        timestamp = datetime.datetime.timestamp(obj.timestamp)
        jalali_datetime = JalaliDateTime.fromtimestamp(timestamp)
        return jalali_datetime.strftime("%Y/%m/%d - %H:%M")

    class Meta:
        model = Message


admin.site.register(Message, MessageAdmin)
