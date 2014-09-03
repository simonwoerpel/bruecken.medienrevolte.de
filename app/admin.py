# -*- coding: utf-8 -*-
"""
Created on Tue Sep  2 19:36:16 2014

@author: simonwoerpel
"""


from django.contrib import admin
from app.models import DataRaw, Bridge, State, Status

# Register your models here.


class DataRawAdmin(admin.ModelAdmin):
    '''The raw dataset is readonly in the admin'''

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    readonly_fields = list_display = DataRaw._meta.get_all_field_names()

    list_filter = ('segment', 'state', 'status', )


class RootModelAdmin(admin.ModelAdmin):
    '''The raw dataset is readonly in the admin'''

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    #readonly_fields = list_display = RootModel._meta.get_all_field_names()

    list_filter = ('segment', 'state', 'status', )


admin.site.register(DataRaw, DataRawAdmin)
admin.site.register(Bridge, RootModelAdmin)
admin.site.register(State)
admin.site.register(Status)
