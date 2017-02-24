# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-22 07:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('focus', '0006_auto_20170222_0701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='posttag',
            field=models.ManyToManyField(to='focus.PostTag', verbose_name='标签'),
        ),
        migrations.AlterField(
            model_name='post',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]