from django.urls import path

from threads.views.thread import ThreadListView

app_name = "threads"
urlpatterns = [
path('', ThreadListView.as_view(), name='thread_list'),
path('threads/', ThreadListView.as_view(), name='thread_list')
]