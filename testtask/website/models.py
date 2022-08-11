from django.conf import settings
from django.db import models

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    id = models.IntegerField(primary_key=True)
    buyer = models.CharField(max_length=100, default='')
    buyer_sub_id = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.user.username



