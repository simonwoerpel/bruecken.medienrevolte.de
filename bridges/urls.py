from django.conf.urls import patterns, include, url
# from django.contrib import admin
from djgeojson.views import TiledGeoJSONLayerView, GeoJSONLayerView
from erm.settings import RootModel

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bridges.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^karte/', 'erm.views.base.show_map'),
    url(r'^tilegeojson/(?P<z>\d+)/(?P<x>\d+)/(?P<y>\d+).geojson$',
        TiledGeoJSONLayerView.as_view(model=RootModel), name='tilegeojson'),
    url(r'^map/(?P<min_lon>[0-9.]+)/(?P<min_lat>[0-9.]+)/(?P<max_lon>[0-9.]+)/(?P<max_lat>[0-9.]+)/(?P<zoom>[0-9]+)$',
        'erm.views.geo.map_cutout'),
    url(r'^data.geojson$', GeoJSONLayerView.as_view(model=RootModel), name='data'),
    url(r'^(.+)', include('erm.urls')),
    url(r'^', 'erm.views.base.index'),
)
