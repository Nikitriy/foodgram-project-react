from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=254, verbose_name='почта')
    username = models.CharField(max_length=150, verbose_name='юзернэйм', unique=True)
    first_name = models.CharField(max_length=150, verbose_name='имя')
    last_name = models.CharField(max_length=150, verbose_name='фамилия')
    password = models.CharField(max_length=150, verbose_name='пароль')

    def __str__(self) -> str:
        return self.username
