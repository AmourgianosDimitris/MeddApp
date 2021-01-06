from django.db import models

# Create your models here.
class Department(models.Model):
    title = models.CharField(max_length=200)
    introduction = models.TextField(null=False, blank=False)
    services = models.TextField(null=False, blank=False)
    diseases = models.TextField(null=False, blank=False)
    preference = models.TextField(null=False, blank=False)

    def __str__(self):
        admin_show = self.title
        return admin_show
#
# class NewsLetter(models.Model):
#     name = models.CharField(max_length=200)
#     email = EmailField(max_length=254, **options)
