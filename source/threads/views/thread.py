from urllib.parse import urlencode

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView

from threads.forms import SimpleSearchForm, ThreadForm
from threads.models.thread import Thread

THREADS_PAGE_SIZE = 10
RESPONSES_PAGE_SIZE = 10


class ThreadListView(ListView):
    template_name = "threads/thread_list.html"
    model = Thread
    context_object_name = "threads"
    paginate_by = THREADS_PAGE_SIZE
    paginate_orphans = 1

    def dispatch(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().dispatch(request, *args, **kwargs)

    def get_search_form(self):
        return SimpleSearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']

    def get_queryset(self):
        queryset = Thread.objects.select_related('author').annotate(
            response_count=Count('responses', distinct=True)
        ).order_by('-created_at')

        if self.search_value:
            queryset = queryset.filter(
                Q(title__icontains=self.search_value) | Q(author__username__icontains=self.search_value)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.form

        if self.search_value:
            context['query'] = urlencode({"search": self.search_value})
            context['search_value'] = self.search_value
        return context

class ThreadCreateView(LoginRequiredMixin, CreateView):
    model = Thread
    form_class = ThreadForm
    template_name = "threads/thread_create.html"
    success_url = reverse_lazy('threads:thread_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Создание темы'
        context['btn_txt'] = 'Сохранить'
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

