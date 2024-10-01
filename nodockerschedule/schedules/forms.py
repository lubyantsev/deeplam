from django import forms
from .models import Schedule, Event


class ScheduleForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Schedule
        fields = ['password']


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['time', 'place', 'participant_name']

class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
