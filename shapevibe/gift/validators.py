import os
from django.core.exceptions import ValidationError

def validate_img_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.png', '.jpg', '.jpeg', '.tif', '.tiff']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')

def validate_audio_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.wav', '.mp3', '.ogg']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')

