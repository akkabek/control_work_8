from django.forms import ModelForm

from threads.models.thread import Thread


class ThreadForm(ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'content']