# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import ListView, DetailView
from erm.views.dynamic import BaseFilterView
from erm.settings import RootModel


class DynamicDetailView(DetailView):

    context_object_name = 'object'

    def get_object(self):
        return BaseFilterView(self.request.path).get_object()

    def get_context_data(self, **kwargs):
        context = super(DynamicDetailView, self).get_context_data(**kwargs)
        for extra_context in BaseFilterView(self.request.path) \
                .get_context_data():
            context[extra_context[0]] = extra_context[1]

        return context

    def get_template_names(self):
        return BaseFilterView(self.request.path).get_template_names()


class RootModelList(ListView):
    model = RootModel


def index(request):
    return render_to_response('erm/index.html',
                              context_instance=RequestContext(request))


def show_map(request):
    return render_to_response('erm/geo/map.html')
