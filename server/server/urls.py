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
    url(r'^success/(booking|return|borrow|admin|insert|)/(\d+)$',views.success),
    url(r'^success/(booking|insert|)/$',views.success),
    #通常响应
    url(r'^$',views.index),
    url(r'^index[/]$',views.index),
    url(r'^search/start/(\d+)/keyword/(.+)',views.search),
    url(r'^collection/',views.collection),
    url(r'^order/bid/(\d+)/uid/(\d+)/err/(\d+)$',views.order),
    url(r'^borrowing/bid/(\d+)/uid/(\d+)/brid/(\d+)/err/(\d+)$',views.borrowing),
    url(r'^subject/(\d+)$',views.subject),
    url(r'^history[/]$',views.history),
    url(r'^history/bid/(\d+)/uid/(\d+)/return/(true|false|null)$',views.history),
    url(r'^index[/]/$',views.index),
    url(r'^insert[/]$',views.insert),
    url(r'^insert/err/(\d+)$',views.insert),
    url(r'^booking/bid/(\d+)/uid/(\d+)/err/(\d+)$',views.booking),
    url(r'^admin/',views.admin),
    url(r'^return/$',views.return1),
    url(r'^return/err/(\d+)$',views.return1),#好吧, 不能用return做函数名
    url(r'^return2/bid/(\d+)/uid/(\d+)/brrid/(\d+)/err/(\d+)$',views.return2),

    #按钮响应
    url(r'^accept/bid/(\d+)/uid/(\d+)/brid/(\d+)$',views.accept_booking),
    url(r'^cancel/bid/(\d*)/uid/(\d+)/brid/(\d+)$',views.cancel_booking),

    #表单响应
    url(r'^SearchAction/',actions.search_action),
    url(r'^BookingAction/(\d+)$',actions.booking_action),
    url(r'^BorrowAction/',actions.borrow_action),
    url(r'^InsertAction/',actions.insert_action),
    url(r'^Return1Action/',actions.return1_action),
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
