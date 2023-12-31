# Generated by Django 4.2.5 on 2023-09-13 05:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("blog", "0008_contact"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="blog",
            name="like_count",
        ),
        migrations.AddField(
            model_name="blog",
            name="like_count",
            field=models.ManyToManyField(
                related_name="blog_like_count", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
