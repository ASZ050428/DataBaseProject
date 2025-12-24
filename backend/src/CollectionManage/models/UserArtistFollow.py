from django.db import models
from django.contrib.auth.models import User
from ArtistManage.models import Artist

class UserArtistFollow(models.Model):
    user_id = models.IntegerField(
        db_column="USER_ID",
        verbose_name="用户ID"
    )
    artist_id = models.IntegerField(
        db_column="ARTIST_ID",
        verbose_name="歌手ID"
    )
    follow_time = models.DateTimeField(auto_now_add=True, db_column="FOLLOW_TIME", verbose_name="关注时间")

    class Meta:
        db_table = "user_follow_artists"
        verbose_name = "用户歌手关注"
        verbose_name_plural = "用户歌手关注"
        unique_together = ("user_id", "artist_id")
