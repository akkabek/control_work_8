from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView

from accounts.forms import MyUserCreationForm
from threads.models.thread import Thread

User = get_user_model()

THREADS_PAGE_SIZE = 10


class RegisterView(CreateView):
    form_class = MyUserCreationForm
    template_name = "accounts/registration.html"
    model = User

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        redirect_url = reverse("threads:thread_list")

        if self.request.GET.get("next"):
            redirect_url = self.request.GET.get("next")

        if self.request.POST.get("next"):
            redirect_url = self.request.POST.get("next")
        return redirect_url

class ProfileDetailView(DetailView):
    model = User
    template_name = "accounts/profile.html"
    context_object_name = "profile_user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['responses_count'] = self.object.responses.count()

        threads_qs = Thread.objects.filter(author=self.object).annotate(
            response_count=Count('responses', distinct=True)
        ).order_by('-created_at')
        paginator = Paginator(threads_qs, THREADS_PAGE_SIZE, orphans=1)
        page_obj = paginator.get_page(self.request.GET.get('page'))

        context['page_obj'] = page_obj
        context['threads'] = page_obj.object_list
        context['is_paginated'] = page_obj.has_other_pages()
        return context
