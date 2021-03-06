from django.conf.urls import patterns, include, url
from django.contrib import admin
from os.path import join

from Hammer.settings import STATICFILES_DIRS

admin.autodiscover()

static_dir = {'document_root': STATICFILES_DIRS[0]}

urlpatterns = patterns(
    '',

    # static files
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', static_dir),

    # admin
    url(r'^admin/',   include(admin.site.urls)),
    url(r'^login$',   'django.contrib.auth.views.login'),
    url(r'^logout$',  'django.contrib.auth.views.logout'),

    # doc views
    url(r'^$',                              'doc.views.home'),
    url(r'^(?P<title>[\w\-_./]+)/missing$', 'doc.views.missing'),
    url(r'^(?P<title>[\w\-_./]+)/(?P<template>[\w\-_./]+)/add$',  'doc.views.add'),
    url(r'^(?P<title>[\w\-_./]+)/edit$',    'doc.views.edit'),
    url(r'^(?P<title>[\w\-_./]+)/delete$',  'doc.views.delete'),
    url(r'^(?P<title>[\w\-_./]+)$',         'doc.views.doc'),

)
