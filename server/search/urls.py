#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^start/(\d+)/keyword/(.+)',views._search),
    url(r'^segment',views.segment),
    url(r'^rebuild/index/?$',views.rebuild_index),
    url(r'^RequestAjaxReindexingBook',views.on_ajax_reindexing_book_request),
)