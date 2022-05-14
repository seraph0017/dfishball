from dataclasses import fields
from rest_framework import serializers
from .models import Media, MediaGroup


class MediaGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaGroup
        fields = ["id", "title", "description",
                  "update_time", "create_time", "group_level"]


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ["id", "title", "description", "pic_time",
                  "upload_user", "group", "upload_file", "is_pic", "create_time", "update_time"]
