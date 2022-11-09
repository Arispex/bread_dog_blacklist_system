from django.db import models
from django.contrib.auth.models import AbstractUser
import system.util


# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="邮箱")
    key = models.CharField(default=system.util.random_str(16), verbose_name="密钥", max_length=16)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name


class Ban(models.Model):
    operator = models.CharField(verbose_name="操作者", max_length=256)
    QQ = models.CharField(verbose_name="封禁QQ", max_length=256)
    reason = models.CharField(verbose_name="原因", max_length=256)
    time = models.DateTimeField(auto_now_add=True, verbose_name="封禁时间")

    def __str__(self):
        return self.QQ

    class Meta:
        verbose_name_plural = "封禁"
        verbose_name = verbose_name_plural