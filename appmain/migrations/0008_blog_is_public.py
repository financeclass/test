# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-10-30 07:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appmain', '0007_blog_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='is_public',
            field=models.BooleanField(default=False),
        ),
    ]