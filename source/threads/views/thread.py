from urllib.parse import urlencode

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DetailView

from threads.forms import SimpleSearchForm, ThreadForm, ResponseForm
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

class ThreadDetailView(LoginRequiredMixin, DetailView):
    model = Thread
    template_name = "threads/thread_detail.html"
    context_object_name = "thread"
    form_class = ResponseForm

    def get_queryset(self):
        return Thread.objects.select_related('author')

    def get_success_url(self):
        return reverse_lazy('threads:thread_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = context.get('form') or self.get_form()

        responses_qs = self.object.responses.select_related('author').annotate(
            author_msg_count=Count('author__responses', distinct=True)
        ).order_by('created_at')

        paginator = Paginator(responses_qs, RESPONSES_PAGE_SIZE, orphans=1)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        context['paginator'] = paginator
        context['responses'] = page_obj.object_list
        context['is_paginated'] = page_obj.has_other_pages()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not request.user.is_authenticated:
            return redirect(f"{reverse_lazy('accounts:login')}?next={request.path}")

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.thread = self.object
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)
