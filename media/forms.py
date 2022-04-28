from django import forms
from django.forms import ModelForm
from django.core.exceptions import NON_FIELD_ERRORS
from django.core.validators import validate_slug
from .models import Media



class MediaUploadForm(forms.Form):

    upload_file = forms.FileField()
    upload_user_id = forms.IntegerField()
    group_id = forms.IntegerField()



class MediaEditForm(ModelForm):
    class Meta:
        model = Media
        fields = ['title', 'description', 'pic_time']