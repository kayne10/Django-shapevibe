from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import datetime

# Create your models here.
class Gift(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    gift_title = models.CharField(max_length=250)
    gift_description = models.TextField(max_length=2000)
    gift_image = models.FileField(null=True, blank=True)
    created_at = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.gift_title + ' - ' + self.user.username


