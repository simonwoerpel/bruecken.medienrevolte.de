# -*- coding: utf-8 -*-
"""
Created on Mon Sep  1 21:27:28 2014

@author: simonwoerpel
"""


import sys
from django.db import IntegrityError
from django.utils.text import slugify
from erm.settings import SLUG_MODELS, RootModel, RawModel
from erm.geoutils import makepoint


EXTRA_PATTERN = False

SOURCE = RawModel

TARGET = RootModel


class Converter(object):
    '''the Converter for `app.models.DataRaw` to `app.models.RootModel`

    the Converter looks for fields in this order:
    1. matching field names outside the `SLUG_MODELS`
    2. performing `SLUG_MODELS` outside `EXTRA_PATTERN`
    3. `EXTRA_PATTERN`'''

    def __init__(self, queryset=False):
        '''initializes the Converter
        queryset should be prepared, e.g. q.filter(converted=False)
        if your machine is multicore you could split the queryset in n
        packages while n is number of cores and run the converter processes
        in different shells simultanously'''

        if not queryset:
            raise Exception('queryset MUST be set')

        else:
            self.S = SOURCE
            self.T = TARGET
            self.P = EXTRA_PATTERN
            self.M = SLUG_MODELS
            self.queryset = queryset
            self.old_fields = [field.name for field in self.S._meta.fields]
            self.extra_fields = [slugify(unicode(m[0].__name__)) for m in self.P] if self.P else []
            self.erm_fields = [slugify(unicode(m.__name__)) for m in self.M if m not in [n[0] for n in self.P]] \
                if self.P else [slugify(unicode(m.__name__)) for m in self.M]
            self.data_only_fields = [field.name for field in RootModel._meta.fields if field.name not in self.erm_fields + self.extra_fields]
            self.extra_model_list = [m[0] for m in self.P] if self.P else []

    def get_test_instance(self):
        return self.queryset.order_by('?')[:1][0]

    def get_target_dict(self, instance):
        '''returns **kwargs for target = TARGET(**kwargs)'''
        if not instance:
            raise Exception('instance MUST be set. \
                    you could use self.get_test_instance()')

        # 1. normal data fields
        d = {}
        for field in self.data_only_fields:
            if field in self.old_fields:
                d[field] = getattr(instance, field)

        # 2. erm fields
        for m in [n for n in self.M if n not in self.extra_model_list]:
            field = slugify(unicode(m.__name__))
            name = getattr(instance, field)
            if not name:
                name = u'Keine Angabe'
            slug = slugify(unicode(name))
            obj, created = m.objects.get_or_create(name=name, slug=slug)
            d[field] = obj

        # 3. extra patterns
        if self.P:
            for m in self.P:
                model = m[0]
                field = slugify(unicode(model.__name__))
                name = getattr(instance, field)
                slug = slugify(unicode(name))

                pattern = [p for p in m[1]]
                extra_dict = {}

                for p in pattern:
                    extra_dict[p[0]] = getattr(instance, p[1])

                obj, created = model.objects.get_or_create(name=name,
                                                           slug=slug,
                                                           **extra_dict)
                d[field] = obj

        ### extra fields ###
        ### don't know how to abstract that this moment

        ## geoutils

        d['geom'] = makepoint(instance)

        ### end of extra operations ###

        return d

    def do_test_convert(self):
        '''returns a TARGET instance from a randomly picked SOURCE instance
        but doesn't save it'''

        try:
            instance = self.queryset.order_by('?')[:1][0]
            t = self.T(**self.get_target_dict(instance))
            r = True
        except:
            r = (False, sys.exc_info())
            t = None

        return r, t

    def do_convert(self):
        '''runs the actual convert if `self.do_test_convert` returns True'''

        if self.do_test_convert()[0]:
            i = 0
            err_i = 0

            for instance in self.queryset:
                try:
                    t = self.T(**self.get_target_dict(instance))
                    t.save()
                    i += 1
                    instance.converted = True
                    instance.save()
                except IntegrityError:
                    err_i += 1
                    instance.convert_error = True
                    instance.convert_error_msg = sys.exc_info()
                    instance.duplicate = True
                    instance.save()
                except:
                    err_i += 1
                    instance.convert_error = True
                    instance.convert_error_msg = sys.exc_info()
                    instance.save()

            return 'succesfully converted %s %s into %s but %s errors.' % \
                        (i, self.S._meta.verbose_name_plural,
                         self.T._meta.verbose_name_plural, err_i)

        else:
            return 'Error: test convert failed.'
