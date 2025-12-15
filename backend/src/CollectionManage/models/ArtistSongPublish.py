from django.db import models
from ArtistManage.models import Artist
from SongManage.models import Song

class ArtistSongPublish(models.Model):
    artist_id = models.ForeignKey(
        Artist, 
        on_delete=models.CASCADE, 
        db_column="ARTIST_ID",
        verbose_name="歌手ID"
    )
    song_id = models.ForeignKey(
        Song, 
        on_delete=models.CASCADE, 
        db_column="SONG_ID",
        verbose_name="歌曲ID"
    )

    class Meta:
        db_table = "artist_song_relation"
        verbose_name = "歌手歌曲发布"
        verbose_name_plural = "歌手歌曲发布"
        unique_together = ("artist_id", "song_id")
