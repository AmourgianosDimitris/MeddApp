from django.contrib import admin
from .models import *
# Register your models here.
admin.site.site_header = 'MedApp Admin'

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('title',)

admin.site.register(Department, DepartmentAdmin)
