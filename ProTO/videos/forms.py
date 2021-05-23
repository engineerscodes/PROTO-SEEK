
from django import forms
from .models import videoUpload


class vd_form(forms.ModelForm):
    class Meta :
        model=videoUpload
        fields=("captions","video")


    def __init__(self, *args, **kwargs):
        super(vd_form, self).__init__(*args, **kwargs)
        self.fields['video'].widget.attrs['id'] = 'video'