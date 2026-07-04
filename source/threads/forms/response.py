from django.forms import ModelForm

from threads.models.response import Response


class ResponseForm(ModelForm):
    class Meta:
        model = Response
        fields = ['message']