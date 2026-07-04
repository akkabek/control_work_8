from django.contrib import admin

from threads.models.thread import Thread
from threads.models.response import Response


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    list_filter = ('author',)
    search_fields = ('title', 'content')


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('thread', 'author', 'created_at')
    list_filter = ('author', 'thread')
