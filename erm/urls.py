# -*- coding: utf-8 -*-
"""
Created on Tue Sep  2 21:10:10 2014

@author: simonwoerpel
"""

from django.conf.urls import url
from erm.views.base import DynamicDetailView


urlpatterns = [
    url(r'^', DynamicDetailView.as_view()),
]
