import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.conf import settings


class MediaGroup(models.Model):

    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_created=True)
    is_active = models.BooleanField(default=True)

    group_level = models.IntegerField(default=2)

    def __str__(self):
        return self.title

    @classmethod
    def get_all_active_group(cls):
        return cls.objects.filter(is_active=True).all()

    @classmethod
    def get_active_group_by_id(cls, id):
        return cls.objects.filter(is_active=True, id=id).first()


def upload_to_place(instance, filename):
    return "{}/{}".format(instance.group.id, filename)


class Media(models.Model):

    title = models.CharField(
        max_length=200, default=settings.DEFAULT_FIELD_STRING)
    description = models.TextField(
        max_length=1000, default=settings.DEFAULT_FIELD_STRING)
    pic_time = models.DateField(default=datetime.date.today)

    upload_file = models.FileField(upload_to=upload_to_place)

    upload_local_file_path = models.CharField(max_length=500)
    upload_oss_file_path = models.CharField(max_length=500)
    upload_cdn_file_path = models.CharField(max_length=500)
    upload_render_file_path = models.CharField(max_length=500)
    upload_user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_pic = models.BooleanField()

    update_time = models.DateTimeField(
        auto_now=True)
    create_time = models.DateTimeField(
        auto_created=True, default=timezone.now)
    is_active = models.BooleanField(default=True)

    group = models.ForeignKey(MediaGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    @classmethod
    def get_active_media_by_media_group_id_in_page(cls, per_page_limit, page_num, media_group_id):
        media_group = MediaGroup.get_active_group_by_id(media_group_id)
        media_list = cls.objects.filter(
            is_active=True, group=media_group).all().order_by('-create_time')
        paginator = Paginator(media_list, per_page_limit)
        page_media = paginator.get_page(page_num)
        return page_media

    @classmethod
    def create_media(cls, upload_file, upload_user_id, group_id):
        is_pic = True
        ext_file_name = upload_file.name.split(".")[-1:].pop()
        if ext_file_name not in ["jpeg", "png", "jpg", "JPG"]:
            is_pic = False
        upload_user = User.objects.filter(id=int(upload_user_id)).first()
        group = MediaGroup.get_active_group_by_id(int(group_id))
        instance = cls(upload_file=upload_file,
                       upload_user=upload_user, group=group, is_pic=is_pic)
        instance.save()
        return True

    @classmethod
    def get_active_media_by_id(cls, media_id):
        return cls.objects.filter(id=media_id, is_active=True).first()

    @classmethod
    def get_all_active_media(cls):
        return cls.objects.filter(is_active=True).all().order_by("-create_time")

    @classmethod
    def get_all_active_photo(cls):
        return cls.objects.filter(is_active=True, is_pic=True).all().order_by("-create_time")

    @classmethod
    def get_all_active_photo_by_media_group_id(cls, media_group_id, limit=10, offset=0):
        group = MediaGroup.get_active_group_by_id(media_group_id)
        return cls.objects.filter(is_active=True, is_pic=True, group=group).all().order_by("-create_time")[offset: offset+limit]
