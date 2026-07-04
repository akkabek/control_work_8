from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def get_avatar_path(instance, filename):
        return f'avatars/{instance.username}/{filename}'

    avatar = models.ImageField(
        upload_to=get_avatar_path,
        verbose_name='Аватар'
    )