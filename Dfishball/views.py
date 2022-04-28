from email import message
from sys import prefix
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from devtools import debug


@login_required()
def password_change_handle(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST.dict())
        debug(request.user)
        debug(request.POST.dict())
        debug(form.errors)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect("logout")
        else:
            messages.error(request, "请查看是否有误")
    raise Http404()
