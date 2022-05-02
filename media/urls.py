from django.urls import path
from rest_framework import routers
from . import views
from . import api

app_name = 'media'

api_router = routers.DefaultRouter()
api_router.register(r'medias', api.MediaApi)
api_router.register(r'mediagroups', api.MediaGroupApi)

urlpatterns = [
    path("", views.media_index_handle, name='index'),
    path("<int:media_id>", views.media_detail_handle, name='detail'),
    path("upload/", views.upload_media_handle, name='upload'),
]
