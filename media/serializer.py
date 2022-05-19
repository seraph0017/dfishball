
from rest_framework import serializers
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)
from .models import Media, MediaGroup
from taggit.models import Tag


class MediaGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaGroup
        fields = ["id", "title", "description",
                  "update_time", "create_time", "group_level"]


class MediaSerializer(serializers.ModelSerializer, TaggitSerializer):

    tags = TagListSerializerField()

    class Meta:
        model = Media
        fields = ["id", "title", "description", "pic_time",
                  "upload_user", "group", "upload_file", "is_pic", "create_time", "update_time", "tags", "upload_local_file_path"]


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = "__all__"
