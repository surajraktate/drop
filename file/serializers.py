from rest_framework import serializers
from .models import File


class FileSerializer(serializers.ModelSerializer):
    class Meta():
        model = File
        fields = ('id', 'file', 'remark', 'room_ip', 'room_name', 'timestamp')
