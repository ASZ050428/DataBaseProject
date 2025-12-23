from django.db import models
from ArtistManage.models import Artist  # 关联艺术家模型

class Song(models.Model):
    song_id = models.AutoField(primary_key=True, verbose_name="歌曲ID")
    title = models.CharField(max_length=200, verbose_name="歌曲标题")
    artist = models.ForeignKey(
        Artist, 
        on_delete=models.CASCADE, 
        related_name="songs",
        verbose_name="所属歌手"
    )
    album_id = models.IntegerField(blank=True, null=True, verbose_name="专辑ID")  # 可改为ForeignKey关联Album
    duration = models.IntegerField(verbose_name="歌曲时长(秒)")
    release_date = models.DateField(verbose_name="发行日期")
    play_count = models.IntegerField(default=0, verbose_name="播放次数")
    audio_url = models.URLField(verbose_name="音频地址")

    class Meta:
        db_table = "song"
        verbose_name = "歌曲"
        verbose_name_plural = "歌曲"
        ordering = ["-play_count"]  # 按播放量倒序排列