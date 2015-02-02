#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from library import views
from library import ajax #专门处理ajax
from library import actions # 专门处理表单
from library import debug #拿来调试用的

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'server.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^success/([a-z]+)$',views.success),
    #通常响应
    url(r'^collection/',views.collection),
    url(r'^order/',views.order),
    url(r'^borrowing/',views.borrowing),
    url(r'^subject/',views.subject),
    url(r'^history/',views.history),
    url(r'^index/',views.index),
    url(r'^insert/',views.insert),

    #表单响应
    url(r'^SearchAction/',actions.search_action),
    url(r'^BookingAction/',actions.booking_action),
    url(r'^BorrowAction/',actions.borrow_action),
    url(r'^InsertAction/',actions.insert_action),
    url(r'^ReturnAction/',actions.return_action),
    url(r'^Return2Action/',actions.return2_action),

    #响应前端的ajax请求
    url(r'^RequestAjaxAdmin/',ajax.on_admin_request),
    url(r'^RequestAjaxPerInfo/',ajax.on_perinfo_request),
    url(r'^RequestAjaxBookInfo/',ajax.on_bookinfo_request),
    url(r'^RequestAjaxInsertBookInfo/',ajax.on_insert_bookinfo_request),

    #处理前端的ajax发送过来的数据
    url(r'^PushAjaxAdmin/',ajax.on_admin_push),

    #调试用
    url(r'^filldb/', debug.filldb),

)
