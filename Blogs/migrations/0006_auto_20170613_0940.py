# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-13 09:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blogs', '0005_cards_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cards',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='Cards', verbose_name='Banner Image for your blog'),
        ),
    ]