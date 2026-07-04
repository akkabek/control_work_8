from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView

from threads.forms import ResponseForm
from threads.mixins import AuthorOrModeratorRequiredMixin
from threads.models.response import Response


class ResponseUpdateView(AuthorOrModeratorRequiredMixin, UpdateView):
    model = Response
    form_class = ResponseForm
    template_name = "threads/response_form.html"
    context_object_name = "response"

    def get_success_url(self):
        return reverse_lazy('threads:thread_detail', kwargs={'pk': self.object.thread_id})

class ResponseDeleteView(AuthorOrModeratorRequiredMixin, DeleteView):
    model = Response
    template_name = "threads/response_confirm_delete.html"
    context_object_name = "response"

    def get_success_url(self):
        return reverse_lazy('threads:thread_detail', kwargs={'pk': self.object.thread_id})