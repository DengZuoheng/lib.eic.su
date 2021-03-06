#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from library import views
from library import ajax #专门处理ajax
from library import actions # 专门处理表单
from library import debug #拿来调试用的
import search

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
    url(r'^collection/',views.collection),
    url(r'^order[/]$',views.order),
    url(r'^order/bid/(\d+)/uid/(\d+)/err/(\d+)/accept/(true|false|null)/borrow/(true|false|null)$',views.order),
    url(r'^borrowing/bid/(\d+)/uid/(\d+)/brid/(\d+)/err/(\d+)$',views.borrowing),
    url(r'^borrowing/$',views.borrowing),
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
    url(r'^upload/$',views.upload),
    url(r'^help/$',views.help),

    #搜索相关
    url(r'^search/', include('search.urls')),

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
    url(r'^PushAjaxUpload/',ajax.on_upload_push),

    #登录
    url(r'^account/', include('login.urls')),

    #验证码
    url(r'^captcha/', include('captcha.urls')),

    #备份还原
    url(r'^backups/',include('backups.urls')),
)
