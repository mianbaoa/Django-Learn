# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-27 01:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('focus', '0012_auto_20170223_0347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posttype',
            name='name',
            field=models.CharField(choices=[('Job', '工作与感情'), ('Python', 'Python学习'), ('Java', 'Java学习'), ('PHP', 'PHP学习')], max_length=10),
        ),
    ]