from urllib.parse import urlencode

from django.db.models import Q
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from threads.forms import SimpleSearchForm
from threads.models.thread import Thread


class ThreadListView(ListView):
    template_name = "threads/list.html"
    model = Thread
    context_object_name = "threads"
    ordering = ["-created_at"]
    queryset = Thread.objects.all()
    paginate_by = 3
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
        queryset = super().get_queryset()

        if self.search_value:
            queryset = queryset.filter(
                Q(title__icontains=self.search_value) | Q(author__icontains=self.search_value)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.form

        if self.search_value:
            context['query'] = urlencode({"search": self.search_value})
            context['search_value'] = self.search_value
        return context