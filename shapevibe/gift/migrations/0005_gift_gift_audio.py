# Generated by Django 2.0.4 on 2018-06-26 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gift', '0004_auto_20180626_1105'),
    ]

    operations = [
        migrations.AddField(
            model_name='gift',
            name='gift_audio',
            field=models.FileField(blank=True, upload_to='audio_files/'),
        ),
    ]
