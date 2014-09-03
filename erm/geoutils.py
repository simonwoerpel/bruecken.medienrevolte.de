# -*- coding: utf-8 -*-
"""
Created on Tue Sep  2 20:09:21 2014

@author: simonwoerpel

geo utils for erm
"""

from django.contrib.gis.geos import Point


def makepoint(instance, lat_field='lat', lon_field='lon'):
    '''returns a `django.contrib.gis.geos.Point` for given instance'''

    if not instance:
        raise Exception('need an instance to perform')

    return Point(float(getattr(instance, lon_field)),
                 float(getattr(instance, lat_field)))


def get_leaflet(instance, geom_field='geom'):
    '''returns lon / lat pair for leaflet.js
    important: `django.contrib.gis.geos.Point` is represented as (lon, lat)
    but leaflet.js needs its coordinates as (lat, lon)!
    '''

    if not instance:
        raise Exception('need an instance to perform')

    lon, lat = getattr(instance, geom_field)
    return '%s, %s' % (round(lat, 4), round(lon, 4))


def get_googlemap(instance, geom_field='geom'):
    '''returns lon / lat pair for google map API
    important: `django.contrib.gis.geos.Point` is represented as (lon, lat)
    but google needs its coordinates as (lat, lon)!
    '''

    if not instance:
        raise Exception('need an instance to perform')

    lon, lat = getattr(instance, geom_field)
    return '%s, %s' % (round(lat, 8), round(lon, 8))


def get_json(instance):
    '''returns json array for `erm.views.geo.map_cutout`'''

    if not instance:
        raise Exception('need an instance to perform')

    lon, lat = instance.geom
    return {
        'name': '<strong><a href="%s">%s</a></strong><br>' %
                (instance.get_absolute_url(), instance),
        'lon': lon,
        'lat': lat,
        'details': '<span class="label label-%s">%s</span>' %
                   (instance.status.bootstrap_flag, instance.status)
    }
