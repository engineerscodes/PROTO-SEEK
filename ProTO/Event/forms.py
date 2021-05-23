
from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ("eventname",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['eventname'].queryset = Event.objects.all()