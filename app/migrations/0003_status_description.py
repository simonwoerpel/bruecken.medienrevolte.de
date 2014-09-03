# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20140902_2003'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='description',
            field=models.CharField(max_length=200, null=True, verbose_name=b'Anmerkungen', blank=True),
            preserve_default=True,
        ),
    ]
