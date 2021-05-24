from django import forms

from .models import TeacherClassRoom


class ClassRoomForm(forms.ModelForm):
    class Meta :
        model=TeacherClassRoom
        fields=("classRoomName",)


    def __init__(self, *args, **kwargs):
        super(ClassRoomForm, self).__init__(*args, **kwargs)
        self.fields['classRoomName'].widget.attrs['placeholder'] = 'WEB TECH LAB'