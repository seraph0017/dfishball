from django.core.management.base import BaseCommand, CommandError
from media.models import Media

class Command(BaseCommand):
    help = '把heic的图片改为jpg'


    def handle(self, *args, **options):
        Media.convert_heic_to_jpg()
        self.stdout.write(self.style.SUCCESS("转化成功"))