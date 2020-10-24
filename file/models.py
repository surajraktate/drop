from django.db import models


# Create your models here.
class FileData(models.Model):
    room_ip = models.CharField(max_length=50, null=True, blank=True)
    room_name = models.CharField(max_length=50, null=True, blank=True)
    file_url = models.CharField(max_length=1001)


class File(models.Model):
    room_ip = models.CharField(max_length=50, null=True, blank=True)
    room_name = models.CharField(max_length=50, null=True, blank=True)
    file = models.FileField(blank=False, null=False)
    remark = models.CharField(max_length=20, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
