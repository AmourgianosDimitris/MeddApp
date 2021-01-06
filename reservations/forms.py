from django import forms
from django.forms import ModelForm, DateField
from .models import Reservation
from django.core.exceptions import ValidationError

def time_to_int(time):
    print('xx')
    time = time.split(':')
    return int(time[0]) * 60 + int(time[1])

class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        # datetime-local is a HTML5 input type, format to make date time show on fields
        fields = '__all__'
