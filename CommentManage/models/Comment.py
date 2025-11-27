from django.db import models
from UserManage.models import User  # 导入UserManage中的User模型

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True, verbose_name="评论ID")
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="comments",
        verbose_name="评论用户"
    )
    song_id = models.IntegerField(verbose_name="歌曲ID")  # 可根据实际情况改为ForeignKey关联Song模型
    content = models.TextField(verbose_name="评论内容")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")

    class Meta:
        db_table = "comment"
        verbose_name = "评论"
        verbose_name_plural = "评论"
        ordering = ["-create_time"]  # 按创建时间倒序排列