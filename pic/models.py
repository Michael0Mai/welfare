from django.db import models
import uuid
import os
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
        verbose_name_plural = "网络图片"
        verbose_name = verbose_name_plural
        unique_together = (('address_web'), )

def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:8], ext)  
    return os.path.join(instance.owner.id, filename) # return the whole path to the file

class beauty_local(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID') # 32位的ID
    file_path = models.ImageField(upload_to = 'uploads', verbose_name='路径')
    file_name = models.TextField(blank=True, null=True, verbose_name='文件名')
    created_time = models.DateTimeField(default=timezone.now, verbose_name='生成时间')
    remark = models.TextField(blank=True, null=True, verbose_name='备注')
    owner = models.ForeignKey('auth.User', on_delete=models.SET("已删除"), related_name = "local_own_by")
    liker = models.ManyToManyField('auth.User', blank=True, null=True, related_name = "local_like_by")
    is_delete = models.BooleanField(default=False)
    def delete(self):
        self.is_delete=True
        self.save()
    def __str__(self): 
        return str(self.file_path)
    class Meta:
        ordering = ['-created_time']
        verbose_name_plural = "本地图片"
        verbose_name = verbose_name_plural
        unique_together = (('file_path'), )

