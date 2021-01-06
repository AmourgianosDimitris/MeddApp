from django.contrib import admin
from .models import *

# Register your models here.
admin.site.site_header = 'MedApp Admin'

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('patient',)

admin.site.register(Reservation, ReservationAdmin)
