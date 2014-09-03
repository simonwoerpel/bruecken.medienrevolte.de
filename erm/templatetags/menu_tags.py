# -*- coding: utf-8 -*-
"""
Created on Thu Aug 21 21:13:47 2014

@author: simonwoerpel

menu tags
"""

from django import template
from erm.settings import MENU_MODELS


register = template.Library()


@register.inclusion_tag('erm/menu.html')
def main_menu():
    '''renders the main menu for the top navbar'''

    menu = []

    for model in MENU_MODELS:
        parent = model._meta.verbose_name_plural
        children = []

        for child in model.objects.all():
            children += [child]

        menu += [{
            'name': parent,
            'children': children,
        }]

    return {'parents': menu}
