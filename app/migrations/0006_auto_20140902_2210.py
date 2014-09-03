# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20140902_2157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bridge',
            name='slug',
            field=models.SlugField(unique=True, verbose_name=b'Slug'),
        ),
    ]
