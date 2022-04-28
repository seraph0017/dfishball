from django.urls import path
from . import views

app_name = 'media'

urlpatterns = [
    path("", views.media_index_handle, name='index'),
    path("<int:media_id>", views.media_detail_handle, name='detail'),
    path("upload/", views.upload_media_handle, name='upload'),
]
