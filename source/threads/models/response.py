from django.contrib.auth import get_user_model
from django.db import models
from threads.models.thread import Thread


class Response(models.Model):
    description = models.TextField(null=True, blank=True, max_length=500, verbose_name='Текст ответа')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.RESTRICT,
        related_name="responses",
        verbose_name="Автор"
    )
    thread = models.ForeignKey(
        Thread,
        on_delete=models.RESTRICT,
        related_name="responses",
        verbose_name="Тема"
    )