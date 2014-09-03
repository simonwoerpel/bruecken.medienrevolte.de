# -*- coding: utf-8 -*-
"""
Created on Sat Aug 16 14:52:35 2014

@author: simonwoerpel

"""


from django.db.models import Sum, Avg, Count
from django.template.loader import render_to_string
from django.utils.text import slugify
from erm.utils import get_statistic_data_for_filter, get_queryset_for_instance
from erm import settings
from erm.settings import RootModel


class DynamicChart(object):
    '''gives charts x and y data for instance
    aggr -- str'''

    def __init__(self, queryset, model, aggr):
        self.queryset = queryset
        self.model = model
        self.aggr = aggr

    def get_chart_data(self):
        '''wraps `app.erm.get_statistic_data_for_filter()` into xdata ydata
        for nvd3-charts
        model -- model to user as filter in queryset
        aggr -- str, which aggregator to use
        '''

        data = get_statistic_data_for_filter(self.model, self.queryset)
        xdata = [d['instance'].name for d in data]
        ydata = [d['value'] for da in data
                for d in da['data'] if d['name'] == self.aggr]

        return xdata, ydata

    def render_nvd3_js(self, charttype='pieChart',
               extra=settings.STANDARD_CHART_EXTRA,
               chartcontainer=settings.STANDARD_CHART_CONTAINER):
        '''renders js data for chart'''

        xdata, ydata = self.get_chart_data()

        template = u'charts/%s_js.html' % slugify(unicode(charttype))

        data = {
            'chartdata': {'x': xdata, 'y': ydata, },
            'charttype': charttype,
            'chartcontainer': chartcontainer,
            'extra': extra,
        }

        return render_to_string(template, data)

    def render_nvd3_div(self, extra_content=None, charttype='pieChart',
                        chartcontainer=settings.STANDARD_CHART_CONTAINER):
        '''renders div container for chart'''

        template = u'charts/%s_div.html' % slugify(unicode(charttype))

        data = {
            'chartcontainer': chartcontainer,
            'extra_content': extra_content,
        }

        return render_to_string(template, data)


def get_charts_for_instance(instance):
    '''returns list of rendered charts for instance based on queryset
    '''

    queryset = get_queryset_for_instance(instance)

    js = []
    divs = []

    for model in settings.FILTER_MODELS:
        if not model == instance._meta.model:
            for aggr in settings.AGGREGATOR_LIST:
                container = u'%s_%s' % (model.__name__, aggr.__name__)
                headline = u'%s (%s)' % (model._meta.verbose_name_plural,
                                              aggr.__name__)
                teaser = u'%s nach %s mit %s: %s' % \
                    (unicode(RootModel._meta.verbose_name_plural),
                     unicode(model._meta.verbose_name_plural),
                     unicode(instance._meta.verbose_name), instance)
                extra_content = '<h4>%s</h4><p>%s</p>' % (headline, teaser)
                chart = DynamicChart(queryset, model, aggr.__name__)
                js += [chart.render_nvd3_js(chartcontainer=container)]
                divs += [chart.render_nvd3_div(chartcontainer=container,
                                               extra_content=extra_content)]

    return js, divs


class DynamicTimeChart(object):
    '''returns a Line Chart based on Time devlopement
    TODO: not abstract yet
    '''

    def __init__(self, field=False, date_group='year',
                 queryset=RootModel.objects.all()):

        if not field:
            raise Exception('field must be set')

        self.field = field
        self.date_group = date_group
        self.queryset = queryset
        self.charttype = 'linePlusBarChart'

    def get_chart_data(self):
        '''returns xdata, ydata1, ydata2'''
        extra_queryset = 'EXTRACT (%s FROM %s)' % (self.date_group,
                                                   self.field)
        data = RootModel.objects \
            .extra({'year': extra_queryset}) \
            .values('year').annotate(n=Count('id'), power=Sum('power'),
                                     power_avg=Avg('power')) \
            .order_by('year')

        xdata = [int(year['year']) for year in data]
        ydata1 = [int(year['n']) for year in data]
        # this has to be abstract...
        ydata2 = [round(year['power'], 1) for year in data]

        return xdata, ydata1, ydata2

    def render_chart(self):
        xdata, ydata1, ydata2 = self.get_chart_data()
        kwargs2 = {'bar': True}

        chartdata = {
            'x': xdata,
            'name1': 'Neue Anlagen', 'y1': ydata1, 'extra1': '',
            'name2': 'Summe kWh neue Anlagen', 'y2': ydata2, 'extra2': '', 'kwargs2': kwargs2,
        }

        data = {
            'charttype': self.charttype,
            'chartdata': chartdata,
            'chartcontainer': 'index_timechart',
            'extra': {'x_is_date': True,
                      'x_axis_format': '%Y'}
        }

        div = render_to_string('charts/chart_div.html', data)
        js = render_to_string('charts/timechart_js.html', data)
        return div, js
