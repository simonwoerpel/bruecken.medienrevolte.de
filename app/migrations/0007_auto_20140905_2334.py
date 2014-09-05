# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20140902_2210'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='route',
            options={'ordering': ['name'], 'verbose_name': 'Strecke', 'verbose_name_plural': 'Strecken'},
        ),
    ]
