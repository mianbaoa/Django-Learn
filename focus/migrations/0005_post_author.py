# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-21 10:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('focus', '0004_post_posttag'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.CharField(default='', max_length=20, verbose_name='作者'),
        ),
    ]
