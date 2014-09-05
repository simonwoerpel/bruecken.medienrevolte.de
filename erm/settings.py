# -*- coding: utf-8 -*-
"""
Created on Mon Sep  1 22:43:52 2014

@author: simonwoerpel

settings for erm
"""


from django.db.models import Count
from app.models import State, Status, Route, Segment, DataRaw, Bridge


RootModel = Bridge
RawModel = DataRaw


SLUG_MODELS = [State, Status, Route, Segment, ]
FILTER_MODELS = [State, Status, Route, Segment, ]
MENU_MODELS = [State, Status, ]

# which fields of which model (basically the `ROOT_MODEL`) will the aggregators
# work with
AGGREGATOR_LIST = (Count, )

AGGREGATORS = [{
    'model': RootModel,
    'fields': [{
        'name': 'status',
        'aggregators': AGGREGATOR_LIST,
    }, ]
}, ]


# if you use german umlauts or other special chars in `Model.verbose_name` you
# have to define `MODEL_LOOKUPS` as a  to get valid models by given slug in urls
MODEL_LOOKUPS = {
    'bruecke': 'bridge',
    'strecke': 'route',
}


# fields to exclude in `app.erm.get_fields_for_instance`

INSTANCE_FIELDS_EXCLUDE = ('id', 'slug', 'bootstrap_flag', )

# Nvd3 Settings
STANDARD_CHART_CONTAINER = 'nvd3chart'

'''
* ``x_is_date`` - if enabled the x-axis will be display as date format
* ``x_axis_format`` - set the x-axis date format, ie. "%d %b %Y"
* ``tag_script_js`` - if enabled it will add the javascript tag '<script>'
* ``jquery_on_ready`` - if enabled it will load the javascript only when page is loaded
    this will use jquery library, so make sure to add jquery to the template.
* ``color_category`` - Define color category (eg. category10, category20, category20c)
'''

STANDARD_CHART_EXTRA = {
    'x_is_date': False,
    'x_axis_format': '',
    'tag_script_js': True,
    'jquery_on_ready': True,
    'show_labels': False,
}
