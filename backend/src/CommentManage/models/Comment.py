from django.db import models
from django.contrib.auth.models import User

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True, verbose_name="评论ID")
    user_id = models.IntegerField(verbose_name="用户ID", default=1)
    song_id = models.IntegerField(verbose_name="歌曲ID") # 歌曲删除时需删除评论
    content = models.TextField(verbose_name="评论内容")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        db_table = "comment"
        verbose_name = "评论"
        verbose_name_plural = "评论"
        ordering = ["-create_time"]  # 按创建时间倒序排列
