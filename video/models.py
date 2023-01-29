from django.db import models
import uuid
from django.utils import timezone

class video_local(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID') # 32位的ID
    file_path = models.FileField(upload_to = 'uploads', verbose_name='路径')
    file_name = models.TextField(blank=True, verbose_name='文件名')
    created_time = models.DateTimeField(default=timezone.now, verbose_name='生成时间')
    remark = models.TextField(blank=True, verbose_name='备注')
    owner = models.ForeignKey('auth.User', on_delete=models.SET("已删除"), related_name = "video_local_own_by")
    liker = models.ManyToManyField('auth.User', blank=True, related_name = "video_local_like_by")
    is_delete = models.BooleanField(default=False)
    def delete(self):
        self.is_delete=True
        self.save()
    def __str__(self): 
        return str(self.file_path)
    class Meta:
        ordering = ['-created_time']
        verbose_name_plural = "本地视频"
        verbose_name = verbose_name_plural
        unique_together = (('file_path'), )

