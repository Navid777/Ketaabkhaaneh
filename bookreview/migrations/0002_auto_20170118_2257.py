# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-18 22:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookreview', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formattedtext',
            name='images',
        ),
        migrations.RemoveField(
            model_name='formattedtext',
            name='videos',
        ),
        migrations.AlterField(
            model_name='article',
            name='text',
            field=models.TextField(),
        ),
        migrations.DeleteModel(
            name='FormattedText',
        ),
    ]
