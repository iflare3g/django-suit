from importlib import import_module
from django.contrib.contenttypes import admin as ct_admin
from django.template.defaulttags import url

tpl_context_class = dict

__all__ = ['import_module', 'ct_admin', 'url', 'tpl_context_class']
