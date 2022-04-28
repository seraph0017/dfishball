import logging
from logging import logMultiprocessing
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import MediaGroup, Media
from .forms import MediaUploadForm, MediaEditForm
from django.conf import settings

logger = logging.getLogger(__name__)

@login_required()
def media_index_handle(request):
    page_num = request.GET.get("page", 1)
    current_user = request.user
    media_group_id = request.GET.get("media_group", 1)
    media_group_list = MediaGroup.get_all_active_group()
    current_media_group = MediaGroup.get_active_group_by_id(media_group_id)
    page_media_list = Media.get_active_media_by_media_group_id_in_page(
        settings.PER_PAGE_LIMIT, page_num, media_group_id)
    context = dict(
        media_group_list=media_group_list,
        current_media_group=current_media_group,
        current_user=current_user,
        page_media_list=page_media_list,
    )
    logger.debug(context)
    return render(request, "media/index.html", context)


@login_required()
def media_detail_handle(request, media_id):
    media = Media.get_active_media_by_id(media_id)
    if request.method == "POST":
        form = MediaEditForm(request.POST)
        if form.is_valid():
            media.title = request.POST.get("title", "")
            media.description = request.POST.get("description", "")
            media.pic_time = request.POST.get("pic_time", "")
            media.save()
        return JsonResponse(dict(message="ok"))
    context = dict(
        media=media,
    )
    return render(request, "media/detail.html", context)


@login_required()
def upload_media_handle(request):
    if request.method == "POST":
        form = MediaUploadForm(request.POST, request.FILES)
        if form.is_valid():
            Media.create_media(request.FILES['upload_file'], request.POST.get(
                'upload_user_id'), request.POST.get('group_id'))
            return JsonResponse(dict(message="ok"))
    return JsonResponse(dict(message="not ok"))
