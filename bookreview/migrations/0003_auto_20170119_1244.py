# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-19 12:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookreview', '0002_auto_20170118_2257'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='secondary_title',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='reference',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='book', to='bookreview.Reference'),
        ),
        migrations.AlterField(
            model_name='film',
            name='reference',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='film', to='bookreview.Reference'),
        ),
        migrations.AlterField(
            model_name='person',
            name='reference',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='person', to='bookreview.Reference'),
        ),
    ]