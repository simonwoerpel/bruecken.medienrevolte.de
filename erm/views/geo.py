# -*- coding: utf-8 -*-
"""
Created on Thu Aug 21 19:31:34 2014

@author: simonwoerpel

geo specific views

TODO: not abstract yet
"""

from django.http import JsonResponse
from django.contrib.gis.geos import Polygon
from erm.settings import RootModel


def map_cutout(request, min_lon, min_lat, max_lon, max_lat, zoom):
    '''returns the `RootModel` instances based on bbox for json leaflet'''
    if not int(zoom) > 12:
        return JsonResponse(None, safe=False)
    else:
        bbox = (float(min_lon), float(min_lat), float(max_lon), float(max_lat))
        box = Polygon.from_bbox(bbox)
        q = RootModel.objects.filter(geom__within=box)
        resp = [p.get_json() for p in q]
        return JsonResponse(resp, safe=False)
