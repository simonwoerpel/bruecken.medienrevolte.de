# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_status_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='bridge',
            name='slug',
            field=models.SlugField(null=True, verbose_name=b'Slug', blank=True),
            preserve_default=True,
        ),
    ]
