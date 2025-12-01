from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True, verbose_name="用户ID")
    username = models.CharField(max_length=50, unique=True, verbose_name="用户名")
    password = models.CharField(max_length=128, verbose_name="用户密码")

    class Meta:
        db_table = "user"
        verbose_name = "用户"
        verbose_name_plural = "用户"