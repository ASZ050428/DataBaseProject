from django.db import models

class Artist(models.Model):
    artist_id = models.AutoField(primary_key=True, verbose_name="歌手ID")
    name = models.CharField(max_length=100, verbose_name="歌手名称")
    avatar = models.URLField(blank=True, null=True, verbose_name="歌手头像")
    introduction = models.TextField(blank=True, null=True, verbose_name="歌手简介")
    birth_date = models.DateField(blank=True, null=True, verbose_name="出生日期")
    genre = models.CharField(max_length=50, blank=True, null=True, verbose_name="音乐风格")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "artist"
        verbose_name = "歌手"
        verbose_name_plural = "歌手"
        ordering = ["name"]  # 按名称正序排列