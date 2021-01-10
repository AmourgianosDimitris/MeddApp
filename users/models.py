from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='+')
    phone = models.CharField(max_length=14)
    address = models.CharField(max_length=200)
    birthdate = models.DateField(default='2020-01-01', verbose_name = u'Ημερομηνία')

    def __str__(self):
        admin_show = self.user
        return admin_show
