from django.db import models


# Create your models here.
class ClipBoardData(models.Model):
    room_ip = models.CharField(max_length=50, null=True, blank=True)
    room_name = models.CharField(max_length=50, null=True, blank=True)
    room_data = models.CharField(max_length=1001)
