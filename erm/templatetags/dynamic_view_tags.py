# -*- coding: utf-8 -*-
"""
Created on Thu Aug 14 22:37:46 2014

@author: simonwoerpel
"""

from django import template
from django.utils.text import slugify
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from erm.utils import get_aggregators, get_fields_for_instance, \
    get_other_instances_of_this_type, get_queryset_for_instance
from erm.settings import RootModel


register = template.Library()


@register.inclusion_tag('erm/instance_table.html')
def get_table_for_instance(instance, table_direction='portrait'):
    '''returns rendered attribute table for given instance
    default table layout is portrait until `table_direction=landscape`
    is given'''

    landscape = False
    field = slugify(unicode(instance._meta.model.__name__))
    queryset = RootModel.objects.filter(**{field: instance})
    fields = get_fields_for_instance(instance) + \
             get_aggregators(queryset, do_round=1)

    if table_direction == 'landscape':
        landscape = True

    return {
        'fields': fields,
        'landscape': landscape,
    }


@register.inclusion_tag('erm/other_instances.html')
def get_other_instances(instance, limit=50):
    '''returns a clickable list of other instances of this type'''

    return {
        'instances': get_other_instances_of_this_type(instance)[:limit],
        'name_plural': instance._meta.verbose_name_plural,
    }


@register.inclusion_tag('erm/object_table.html', takes_context=True)
def object_table(context, instance=False, random=False):
    '''returns a table for the RootModel, if instance given it will be filtered
    '''

    if instance:
        queryset = get_queryset_for_instance(instance)
    else:
        queryset = RootModel.objects.all()

    if random:
        queryset = queryset.order_by('?')

    request = context['request']

    paginator = Paginator(queryset, 25)  # Show 25 contacts per page

    page = request.GET.get('p')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        objects = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        objects = paginator.page(paginator.num_pages)

    return {'objects': objects}
