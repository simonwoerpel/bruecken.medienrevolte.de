# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataRaw',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('segment', models.CharField(max_length=200, verbose_name=b'Netzsegment')),
                ('route', models.CharField(max_length=4, verbose_name=b'Streckennr')),
                ('status', models.CharField(max_length=1, verbose_name=b'Zustandskategorie')),
                ('state', models.CharField(max_length=200, verbose_name=b'Bundesland')),
                ('lon', models.CharField(max_length=50, verbose_name=b'Lon')),
                ('lat', models.CharField(max_length=50, verbose_name=b'Lat')),
            ],
            options={
                'verbose_name': 'Br\xfccke',
                'verbose_name_plural': 'Br\xfccken',
            },
            bases=(models.Model,),
        ),
    ]
