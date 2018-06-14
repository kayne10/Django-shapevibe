from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import datetime

# Create your models here.
class Gift(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    gift_title = models.CharField(max_length=250)
    gift_description = models.TextField(max_length=2000)
    gift_image = models.FileField(blank=True)
    created_at = models.DateField(default=datetime.date.today)


    def __str__(self):
        return self.gift_title + ' - ' + self.user.username

# class Tag(models.Model):
#     name = models.CharField(max_length=25, on_delete=models.CASCADE, blank=True, null=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=15, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    summary = models.TextField(max_length=500, blank=True)
    avatar = models.FileField(upload_to='avatars/', blank=True)
    # tags are for Postgres db only

    user.is_active = True

    def __str__(self):
        return self.user.username + ': ' + self.first_name + ' ' + self.last_name

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
