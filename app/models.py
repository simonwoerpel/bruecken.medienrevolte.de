# -*- coding: utf-8 -*-
"""
Created on Tue Sep  2 19:25:09 2014

@author: simonwoerpel

models for bridges app

inspired by http://www.zeit.de/mobilitaet/2014-09/deutsche-bahn-bruecken-zustand
info: http://blog.zeit.de/open-data/2014/09/02/deutsche-bahn-bruecken-daten/
data: https://docs.google.com/spreadsheets/d/1z2zpPexIcGagV9qGeeIRct0u5BfMOdHut6vKl2nY8rk/edit#gid=252127531

"""

from django.utils.text import slugify
from django.db import models
from django.contrib.gis.db import models as gismodels
from django.contrib.sites.models import Site
from erm.models import AbstractNameSlugModel
from erm import geoutils

# Create your models here.


class DataRaw(models.Model):
    segment = models.CharField('Netzsegment', max_length=200)
    route = models.CharField('Streckennr', max_length=4)
    status = models.CharField('Zustandskategorie', max_length=1)
    state = models.CharField('Bundesland', max_length=200)
    lon = models.CharField('Lon', max_length=50)
    lat = models.CharField('Lat', max_length=50)

    class Meta:
        verbose_name = 'Brücke'
        verbose_name_plural = 'Brücken'

    def __unicode__(self):
        return '%s, %s - %s' % (self.state, self.segment, self.route)


class State(AbstractNameSlugModel):
    class Meta:
        verbose_name = u'Bundesland'
        verbose_name_plural = u'Bundesländer'
        ordering = ['name']


class Status(AbstractNameSlugModel):
    bootstrap_flag = models.CharField('Bootstrap Farbe', max_length=50,
                                      blank=True, null=True)
    description = models.CharField('Anmerkungen', max_length=200,
                                   blank=True, null=True)

    class Meta:
        verbose_name = u'Zustandskategorie'
        verbose_name_plural = u'Zustandskategorien'
        ordering = ['name']


class Route(AbstractNameSlugModel):
    class Meta:
        verbose_name = u'Streckennummer'
        verbose_name_plural = u'Streckennummern'
        ordering = ['name']


class Segment(AbstractNameSlugModel):
    class Meta:
        verbose_name = u'Netzsegment'
        verbose_name_plural = u'Netzsegmente'
        ordering = ['name']


class Bridge(gismodels.Model):
    slug = models.SlugField('Slug', unique=True, db_index=True)
    segment = gismodels.ForeignKey(Segment, verbose_name='Netzsegment')
    route = gismodels.ForeignKey(Route, verbose_name='Streckennummer')
    state = gismodels.ForeignKey(State, verbose_name='Bundesland')
    status = gismodels.ForeignKey(Status, verbose_name='Zustandskategorie')
    geom = gismodels.PointField()

    objects = gismodels.GeoManager()

    def __unicode__(self):
        return u'%s, %s - %s' % (self.state, self.segment, self.route)

    def get_leaflet(self):
        return geoutils.get_leaflet(self)

    def get_googlemap(self):
        return geoutils.get_googlemap(self)

    def get_json(self):
        return geoutils.get_json(self)

    def get_absolute_url(self):
        return u'http://' + Site.objects.get_current().domain + \
            u'/bruecke:%s/' % self.slug

    class Meta:
        verbose_name = 'Eisenbahnbrücke'
        verbose_name_plural = 'Eisenbahnbrücken'
