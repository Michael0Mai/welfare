from django.db import models
import uuid
from django.utils import timezone

class beauty(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID') # 32位的设备ID
    address_web = models.URLField(max_length=200, blank=True, null=True, verbose_name='网址')
    created_time = models.DateTimeField(default=timezone.now, verbose_name='生成时间')
    remark = models.TextField(blank=True, null=True, verbose_name='备注')
    owner = models.ForeignKey('auth.User', on_delete=models.SET("已删除"), related_name = "own_by")
    liker = models.ManyToManyField('auth.User', blank=True, null=True, related_name = "like_by")
    is_delete = models.BooleanField(default=False)
    def delete(self):
        self.is_delete=True
        self.save()
    def __str__(self): 
        return self.address_web
    class Meta:
        ordering = ['-created_time']
        verbose_name_plural = "图片"
        verbose_name = verbose_name_plural
        unique_together = (('address_web'), )
