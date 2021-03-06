import datetime
import pyheif


from PIL import Image
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.conf import settings

from taggit.managers import TaggableManager

from devtools import debug


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


def upload_to_place_in_upload(group_id, filename):
    return "{}/{}".format(group_id, filename)


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

    tags = TaggableManager()

    def __str__(self):
        return self.title

    @classmethod
    def get_active_media_by_media_group_id_in_page(cls, per_page_limit, page_num, media_group_id, tags):
        media_group = MediaGroup.get_active_group_by_id(media_group_id)
        if tags:
            media_list = cls.objects.filter(
                is_active=True, group=media_group, tags__name__in=tags).all().order_by('-pic_time')
        else:
            media_list = cls.objects.filter(
                is_active=True, group=media_group).all().order_by('-pic_time')

        paginator = Paginator(media_list, per_page_limit)
        page_media = paginator.get_page(page_num)
        return page_media

    @classmethod
    def create_media(cls, upload_file, upload_user_id, group_id):
        is_pic = True
        ext_file_name = upload_file.name.split(".")[-1:].pop()
        if ext_file_name.lower() not in ["jpeg", "png", "jpg", "heic"]:
            is_pic = False
        upload_user = User.objects.filter(id=int(upload_user_id)).first()
        group = MediaGroup.get_active_group_by_id(int(group_id))
        instance = cls(upload_file=upload_file, upload_local_file_path=upload_to_place_in_upload(group.id, upload_file.name),
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
        return cls.objects.filter(is_active=True, is_pic=True, group=group).all().order_by("-pic_time")[offset: offset+limit]

    @classmethod
    def get_all_active_photo_by_tags(cls, media_group_id, tags, limit=10, offset=0):
        if tags:
            group = MediaGroup.get_active_group_by_id(media_group_id)
            return cls.objects.filter(is_active=True, is_pic=True, group=group, tags__name__in=tags).all().order_by("-pic_time")[offset: offset+limit]
        return cls.get_all_active_photo_by_media_group_id(media_group_id, limit=limit, offset=offset)

    @classmethod
    def convert_heic_to_jpg_once(cls):
        all_media = cls.get_all_active_media()
        for media in all_media:
            if media.upload_file.name.lower().endswith(".heic"):
                ori_file_name = "".join(media.upload_file.name.split(".")[:-1])
                jpg_file_name = ori_file_name + ".jpeg"
                full_jpg_file_name = settings.BASE_DIR / \
                    ("upload/" + jpg_file_name)
                try:
                    heif_file = pyheif.read(media.upload_file.read())
                    image = Image.frombytes(heif_file.mode, heif_file.size,
                                            heif_file.data, "raw", heif_file.mode, heif_file.stride)
                    image.save(full_jpg_file_name, "JPEG")
                    media.upload_local_file_path = jpg_file_name
                    media.is_pic = True
                    media.save()
                except Exception as e:
                    print(e)
            else:
                media.upload_local_file_path = media.upload_file.name
                media.save()

    @classmethod
    def convert_heic_to_jpg(cls):
        all_media = cls.get_all_active_media()
        for media in all_media:
            if media.upload_local_file_path.lower().endswith(".heic"):
                ori_file_name = "".join(media.upload_file.name.split(".")[:-1])
                jpg_file_name = ori_file_name + ".jpeg"
                full_jpg_file_name = settings.BASE_DIR / \
                    ("upload/" + jpg_file_name)
                try:
                    heif_file = pyheif.read(media.upload_file.read())
                    image = Image.frombytes(heif_file.mode, heif_file.size,
                                            heif_file.data, "raw", heif_file.mode, heif_file.stride)
                    image.save(full_jpg_file_name, "JPEG")
                    media.upload_local_file_path = jpg_file_name
                    media.is_pic = True
                    media.save()
                except Exception as e:
                    print(e)
                    continue
