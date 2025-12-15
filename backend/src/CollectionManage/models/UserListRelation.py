from django.db import models
from django.contrib.auth.models import User
from CollectionManage.models import CollectionList

class UserListRelation(models.Model):
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="USER_ID",
        verbose_name="用户ID"
    )
    list_id = models.ForeignKey(
        CollectionList,
        on_delete=models.CASCADE,
        db_column="LIST_ID",
        verbose_name="表ID"
    )

    class Meta:
        db_table = "user_list_relation"
        verbose_name = "用户收藏列表关联"
        verbose_name_plural = "用户收藏列表关联"
        unique_together = ("user_id", "list_id")
