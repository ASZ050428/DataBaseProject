from django.db import models
from ArtistManage.models import Artist

class Album(models.Model):
    album_id = models.AutoField(primary_key=True, verbose_name="专辑ID")
    album_name = models.CharField(max_length=100, verbose_name="专辑名")
    release_time = models.DateField(verbose_name="发布时间")
    singer_id = models.ForeignKey(
        Artist, 
        on_delete=models.CASCADE, 
        db_column="album_artist_id",
        related_name="albums",
        verbose_name="专辑歌手ID"
    )

    class Meta:
        db_table = "album"
        verbose_name = "专辑"
        verbose_name_plural = "专辑"