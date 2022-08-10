from django.conf import settings
from django.db import models

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    id = models.IntegerField(primary_key=True)

    def __str__(self):
        return self.user.username



