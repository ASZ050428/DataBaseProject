from django.db import models

class Artist(models.Model):
    artist_id = models.AutoField(primary_key=True, verbose_name="歌手ID")
    artist_name = models.CharField(max_length=100, verbose_name="歌手名称")
    region = models.CharField(max_length=100, blank=True, null=True, verbose_name="地区")
    bio = models.TextField(blank=True, null=True, verbose_name="简介")

    class Meta:
        db_table = "artist"
        verbose_name = "歌手"
        verbose_name_plural = "歌手"
        ordering = ["artist_name"]  # 按名称正序排列