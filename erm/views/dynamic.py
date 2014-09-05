# -*- coding: utf-8 -*-
"""
Created on Thu Aug 14 20:56:23 2014

@author: simonwoerpel

"""


from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from erm.settings import MODEL_LOOKUPS, RootModel
from erm.utils import get_queryset_for_instance
from erm.views.charts import get_charts_for_instance


class BaseFilterView(object):
    '''delivers required arguments for `app.views.base.DynamicListView` based
    on the given `url`
    '''

    def __init__(self, url):
        '''urls have to be in format like '/model1:instance1/model2:instance2/
        '''
        try:
            url = url.replace('/', '')
            model, instance = url.split(':')
        except:
            raise Http404

        try:
            self.model = ContentType.objects.get(name__iexact=model)
        except ContentType.DoesNotExist:
            try:
                model_name = MODEL_LOOKUPS[model]
            except KeyError:
                raise Http404

            self.model = ContentType.objects.get(model=model_name)

        try:
            self.instance = self.model.get_object_for_this_type(slug=instance)
        except ObjectDoesNotExist:
            raise Http404

        self.queryset = get_queryset_for_instance(self.instance) \
            if not self.model.model_class() == RootModel else None
        self.template_name = 'erm/dynamic_detail.html' \
            if not self.model.model_class() == RootModel \
            else 'app/bridge_detail.html'

    def get_template_names(self):
        return [self.template_name, ]

    def get_object(self):
        '''returns the actual object instance'''
        return self.instance

    def get_context_data(self):
        '''returns extra context for given view'''
        #chart_js, chart_divs = get_charts_for_instance(self.instance)
        return [
            ['object_name', self.get_object()._meta.verbose_name, ],
        #    ['chart_js', chart_js, ],
        #    ['chart_divs', chart_divs, ],
        ]
