# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bridge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('geom', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
            options={
                'verbose_name': 'Eisenbahnbr\xfccke',
                'verbose_name_plural': 'Eisenbahnbr\xfccken',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name=b'Name')),
                ('slug', models.SlugField(max_length=200, verbose_name=b'Slug')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Streckennummer',
                'verbose_name_plural': 'Streckennummern',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Segment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name=b'Name')),
                ('slug', models.SlugField(max_length=200, verbose_name=b'Slug')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Netzsegment',
                'verbose_name_plural': 'Netzsegmente',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name=b'Name')),
                ('slug', models.SlugField(max_length=200, verbose_name=b'Slug')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Bundesland',
                'verbose_name_plural': 'Bundesl\xe4nder',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name=b'Name')),
                ('slug', models.SlugField(max_length=200, verbose_name=b'Slug')),
                ('bootstrap_flag', models.CharField(max_length=50, null=True, verbose_name=b'Bootstrap Farbe', blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Zustandskategorie',
                'verbose_name_plural': 'Zustandskategorien',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='bridge',
            name='route',
            field=models.ForeignKey(verbose_name=b'Streckennummer', to='app.Route'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bridge',
            name='segment',
            field=models.ForeignKey(verbose_name=b'Netzsegment', to='app.Segment'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bridge',
            name='state',
            field=models.ForeignKey(verbose_name=b'Bundesland', to='app.State'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bridge',
            name='status',
            field=models.ForeignKey(verbose_name=b'Zustandskategorie', to='app.Status'),
            preserve_default=True,
        ),
    ]
