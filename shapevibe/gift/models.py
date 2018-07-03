from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .validators import validate_img_file_extension, validate_audio_file_extension
import datetime

# Create your models here.
class Gift(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    gift_title = models.CharField(max_length=250)
    gift_description = models.TextField(max_length=2000)
    gift_image = models.FileField(blank=True, validators=[validate_img_file_extension])
    gift_audio = models.FileField(upload_to='audio_files/', blank=True, validators=[validate_audio_file_extension])
    price = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    tags = ArrayField(models.CharField(max_length=50), blank=True, null=True, default=[])
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.gift_title + ' - ' + self.user.username

    def split_tags(self):
        return self.tags.split(',')

    def handle_tags_when_free(self):
        if self.price is None or 0:
            self.tags.append('free')
        else:
            if 'free' in self.tags:
                self.tags.remove('free')
        return self.tags

    # def save(self, force_insert=False, force_update=False):
    #     super(Gift, self).save(force_insert, force_update)
    #
    #     if self.id is not None:
    #         previous = Gift.objects.get(id=self.id)
    #         if self.gift_image and self.gift_image != previous.gift_image:
    #             image = Image.open(self.gift_image.path)
    #             image = image.resize((96, 96), Image.ANTIALIAS)
    #             image.save(self.gift_image.path)

# class Tag(models.Model):
#     name = models.CharField(max_length=25, on_delete=models.CASCADE, blank=True, null=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=15, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    summary = models.TextField(max_length=500, blank=True)
    avatar = models.FileField(upload_to='avatars/', blank=True, validators=[validate_img_file_extension])
    tags = ArrayField(models.CharField(max_length=50), blank=True, null=True, default=[])
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + ': ' + self.first_name + ' ' + self.last_name

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    # def save(self, force_insert=False, force_update=False):
    #     super(Profile, self).save(force_insert, force_update)
    #
    #     if self.id is not None:
    #         previous = Profile.objects.get(id=self.id)
    #         if self.avatar and self.avatar != previous.avatar:
    #             image = Image.open(self.avatar.path)
    #             image = image.resize((96, 96), Image.ANTIALIAS)
    #             image.save(self.avatar.path)
