# -*- coding: utf-8 -*-
"""
Created on Thu Aug 21 23:36:44 2014

@author: simonwoerpel

geo related templatetags
"""


from django import template
from django.contrib.gis.measure import D
from erm.settings import RootModel


register = template.Library()


@register.inclusion_tag('erm/geo/nearby.html')
def nearby(instance, n=10):
    '''returns nearby items of the given instnace'''

    if not instance.geom:
        return {
            'no_geopoint_error': True,
            'instance': instance,
        }

    else:
        ref = instance.geom
        return {'object_list': RootModel.objects
                               .exclude(geom__isnull=True)
                               .exclude(id=instance.id)
                               .filter(geom__distance_lte=(ref, D(km=100)))
                               .distance(ref).order_by('distance')[1:n+1],
        }


@register.simple_tag
def geocode(source, instance):
    '''geocodes given instance'''

    if source == 'google':
        if not instance.geom_source == 'google':
            #instance.set_coords(source=source)

            return '<div class="alert alert-warning" role="alert"> \
                      %s ist noch nicht richtig geocodiert.</div>' % instance

        else:
            return '<div class="alert alert-info" role="alert"> \
                      %s ist bereits geocodiert.</div>' % instance
