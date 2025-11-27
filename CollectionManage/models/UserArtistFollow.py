from django.db import models
from UserManage.models import User
from ArtistManage.models import Artist as Singer

class UserSingerFollow(models.Model):
    user_id = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        db_column="user_id",
        verbose_name="用户ID"
    )
    singer_id = models.ForeignKey(
        Singer, 
        on_delete=models.CASCADE, 
        db_column="singer_id",
        verbose_name="歌手ID"
    )
    follow_time = models.DateTimeField(auto_now_add=True, verbose_name="关注时间")

    class Meta:
        db_table = "user_singer_follow"
        verbose_name = "用户歌手关注"
        verbose_name_plural = "用户歌手关注"
        unique_together = ("user_id", "singer_id")  # 组合主键