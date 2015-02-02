#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django import template
from django.shortcuts import render_to_response
from library.models import Book
from django.http import HttpResponse
from django.template import RequestContext

# Create your views here.
def collection(request):
    book_list=list(Book.objects.all())
    return render_to_response('collection.html', {'book_list': book_list})

def order(reuqest):
    order_list=list(BookingRecord.objects.all().order_by('-bdate'))
    return render_to_response('order.html',{'order_list':order_list})

def borrowing(reuqesst):
    pass

def subject(request):
    pass

def history(request):
    pass

def index(request):
    pass

def insert(request):
    return  render_to_response('insert.html',context_instance=RequestContext(request))

def success(request,type):
    success_dict={
        'booking':False,
        'return':False,
        'borrow':False,
        'admin':False,
        'insert':False,
        'back_href':'/index/',
        'github':'https://github.com/DengZuoheng/lib.eic.su/issues'
    }

    if(type=='insert'):
        success_dict['back_href']='/insert/'
        success_dict['insert']=True
    elif(type=='admin'):
        success_dict['back_href']='/admin/'
        success_dict['admin']=True
    elif(type=='borrow'):
        success_dict['back_href']='/borrow/'
        success_dict['borrow']=True
    elif(type=='return'):
        success_dict['back_href']='/return/'
        success_dict['return']=True
    return render_to_response('success.html',{'success':success_dict})