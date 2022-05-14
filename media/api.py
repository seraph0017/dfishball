from urllib import response
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, mixins
from django.http import HttpResponse
from .serializer import MediaGroupSerializer, MediaSerializer
from .models import MediaGroup, Media
from django.shortcuts import get_object_or_404
from devtools import debug


class MediaGroupApi(viewsets.ModelViewSet):

    queryset = MediaGroup.get_all_active_group()
    serializer_class = MediaGroupSerializer


class MediaGroupListApi(generics.ListAPIView):

    queryset = MediaGroup.get_all_active_group()
    serializer_class = MediaGroupSerializer


class MediaApi(viewsets.ModelViewSet):

    queryset = Media.get_all_active_photo()
    serializer_class = MediaSerializer


class MediaListApi(APIView):

    def get(self, request):
        media_group_id = int(request.query_params.get('media_group_id', "1"))
        limit = int(request.query_params.get('limit', "10"))
        offset = int(request.query_params.get('offset', "0"))
        media_list = Media.get_all_active_photo_by_media_group_id(media_group_id, limit, offset)
        serializer = MediaSerializer(media_list, many=True)
        return Response(serializer.data)

    def post(self, request):
        f = request.FILES.get("filePath")
        Media.create_media(f, request.POST.get(
                'upload_user_id'), request.POST.get('group_id'))
        return Response(dict(message="ok"))


class MediaDetailApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = Media.get_all_active_photo()
    serializer_class = MediaSerializer
    lookup_field = 'media_id' 

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        media_id = kwargs.get("media_id")
        obj = Media.get_active_media_by_id(media_id)
        obj.title = request.data.get("title")
        obj.description = request.data.get("description")
        obj.save()
        return Response(dict(message="ok"))

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        filter["id"] = self.kwargs[self.lookup_field]
        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

