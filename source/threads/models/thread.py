from django.db import models
from django.contrib.auth import get_user_model

class Thread(models.Model):
    title = models.CharField(max_length=70, verbose_name='Название темы')
    content = models.TextField(max_length=500, verbose_name='Содержимое темы')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.RESTRICT,
        related_name="threads",
        verbose_name="Автор"
    )