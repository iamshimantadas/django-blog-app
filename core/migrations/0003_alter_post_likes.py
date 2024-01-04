# Generated by Django 5.0 on 2023-12-27 11:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_post_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(null=True, related_name='like', to=settings.AUTH_USER_MODEL),
        ),
    ]