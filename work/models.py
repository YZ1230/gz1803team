from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class MyUser(AbstractUser):
    phone = models.CharField(
        verbose_name='手机号码',
        max_length=13,
        unique=True
    )
    email = models.EmailField(
        verbose_name='邮箱'
    )
    icon = models.FileField(
        null=True
    )


