# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-08-16 14:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appmain', '0005_blog_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='channel',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='type',
            field=models.IntegerField(null=True),
        ),
    ]