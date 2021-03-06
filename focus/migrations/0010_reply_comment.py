# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-23 02:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('focus', '0009_poll'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reply_Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(default='')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published')),
                ('replied_comment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='focus.Comment')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
