"""Dfishball URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from .views import password_change_handle
from media.urls import api_router
from media.api import MediaGroupListApi, MediaListApi, MediaDetailApi
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

from .api_auth import FTokenObtainPairView


urlpatterns = [
    path("", RedirectView.as_view(pattern_name="media:index", permanent=False)),
    path("media/", include("media.urls")),
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(next_page="media:index")),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page="login")),
    path('accounts/password_change/',
         password_change_handle, name="password_change"),
    path('accounts/', include('django.contrib.auth.urls')),
    # base api
    # path('api/', include(api_router.urls)),
    path('api/mediagroup/', MediaGroupListApi.as_view(), name="api_media_group_list"),
    path('api/media/', MediaListApi.as_view(), name="api_media_list"),
    path('api/media/<int:media_id>/', MediaDetailApi.as_view(), name="api_media_detail"),
    # session auth
    path('api-auth/', include('rest_framework.urls', namespace="rest_framework")),
    # jwt auth
    path('api/token/', FTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
