from django.conf.urls import include, url
# from django.contrib import admin
from djgeojson.views import TiledGeoJSONLayerView, GeoJSONLayerView
from erm.settings import RootModel
from erm.views import base, geo

urlpatterns = [
    url(r'^karte/', base.show_map),
    url(r'^tilegeojson/(?P<z>\d+)/(?P<x>\d+)/(?P<y>\d+).geojson$',
        TiledGeoJSONLayerView.as_view(model=RootModel), name='tilegeojson'),
    url(r'^map/(?P<min_lon>[0-9.]+)/(?P<min_lat>[0-9.]+)/(?P<max_lon>[0-9.]+)/(?P<max_lat>[0-9.]+)/(?P<zoom>[0-9]+)$',
        geo.map_cutout),
    url(r'^data.geojson$', GeoJSONLayerView.as_view(model=RootModel), name='data'),
    url(r'^(.+)', include('erm.urls')),
    url(r'^', base.index),
]
