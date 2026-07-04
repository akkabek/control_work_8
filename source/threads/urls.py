from django.urls import path

from threads.views.thread import ThreadListView, ThreadCreateView, ThreadDetailView

app_name = "threads"
urlpatterns = [
    path('', ThreadListView.as_view(), name='thread_list'),
    path('threads/', ThreadListView.as_view(), name='thread_list'),
    path('threads/create/', ThreadCreateView.as_view(), name='thread_create'),
    path('threads/<int:pk>/', ThreadDetailView.as_view(), name='thread_detail'),
]