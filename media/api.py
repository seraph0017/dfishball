from rest_framework import viewsets
from .serializer import MediaGroupSerializer, MediaSerializer
from .models import MediaGroup, Media


class MediaGroupApi(viewsets.ModelViewSet):

    queryset = MediaGroup.get_all_active_group()
    serializer_class = MediaGroupSerializer


class MediaApi(viewsets.ModelViewSet):

    queryset = Media.get_all_active_photo()
    serializer_class = MediaSerializer
