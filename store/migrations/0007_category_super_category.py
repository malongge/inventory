# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-14 08:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_auto_20161014_1120'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='super_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.Category', verbose_name='所属分类'),
        ),
    ]