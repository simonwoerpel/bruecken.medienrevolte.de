# -*- coding: utf-8 -*-
"""
Created on Tue Sep  2 20:18:13 2014

@author: simonwoerpel
"""

import urllib2
import StringIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.text import slugify
from erm.settings import AGGREGATORS, RootModel, FILTER_MODELS, \
    INSTANCE_FIELDS_EXCLUDE


def fetch_remote_image(instance=False, urlfield='imgurl', imgfield='img',
                       img_format='jpeg'):
    '''fetches a remote image for given instance and saves it to `ImageField`
    '''
    if not instance:
        raise Exception('need an instance to perform')

    url = getattr(instance, urlfield)
    img = urllib2.urlopen(url).read()

    try:
        image = Image.open(StringIO.StringIO(img))
        image_io = StringIO.StringIO()
        image.save(image_io, format=img_format)
        img_name = '%s.jpg' % instance.id
        img_file = InMemoryUploadedFile(image_io, None, img_name, 'image/jpeg',
                                        image_io.len, None)
        setattr(instance, imgfield, img_file)
        instance.save()

    except Exception, e:
    # The image is not valid
        raise e


def get_queryset_for_instance(instance):
    '''returns the filtered queryset of `RootModel` for given instance'''
    field = slugify(unicode(instance._meta.model.__name__))
    queryset = RootModel.objects.filter(**{field: instance})
    return queryset


def get_other_instances_of_this_type(instance):
    '''returns all *other* instances of same model'''
    return instance._meta.model.objects.exclude(pk=instance.id)


def get_fields_for_instance(instance):
    '''returns field -- value pairs for given instance to render in template
    e.g. in table'''

    fields = []

    for field in instance._meta.fields:
        if not field.name in INSTANCE_FIELDS_EXCLUDE:
            fields += [{
                'name': field.verbose_name,
                'value': getattr(instance, field.name)
            }]

    return fields


def get_aggregators(queryset, do_round=False):
    '''returns aggregator data for given quersyet based on the pattern in
    `app.settings.AGGREGATORS`
    queryset -- the filtered queryset from `app.views.dynamic.BaseFilterView`
    '''

    #if not queryset:
    #    queryset = ROOT_MODEL.objects.all()

    aggrs = []

    for m in AGGREGATORS:
        for field in m['fields']:
            for aggr in field['aggregators']:
                aggr_i = field['name'] + '__' + aggr.__name__.lower()
                value = queryset.aggregate(aggr(field['name']))[aggr_i]
                if do_round:
                    value = round(value, do_round)
                if not value:
                    value = 0
                aggrs += [{
                    'name': aggr.__name__,
                    'value': int(value),
                }, ]

    return aggrs


def get_statistic_data_for_filter(model, queryset):
    '''returns statistics for `FILTER_MODELS`
    '''
    if not model in FILTER_MODELS:
        raise Exception('given model not in FILTER_MODELS')

    data = []
    for instance in model.objects.all():
        field = slugify(unicode(instance._meta.model.__name__))
        data += [{
            'instance': instance,
            'data': get_aggregators(queryset.filter(**{field: instance})),
        }, ]

    return data
