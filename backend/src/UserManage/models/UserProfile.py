from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    realName = models.CharField(max_length=100, blank=True, default='')
    gender = models.CharField(max_length=10, blank=True, default='')
    birthday = models.DateField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    roles = models.CharField(max_length=200, blank=True, default='')
    daily_calories_burn_goal = models.IntegerField(null=True, blank=True)
    daily_calories_intake_goal = models.IntegerField(null=True, blank=True)
    daily_sleep_hours_goal = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'user_profile'
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料'
