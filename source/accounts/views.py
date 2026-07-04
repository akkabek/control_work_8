from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView

from accounts.forms import MyUserCreationForm

User = get_user_model()


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