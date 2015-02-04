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

def booking(request,book_id,user_account,error_id):
    booking_item=None
    user_item=None
    error_item=None
    if('0'!=user_account):
        try:
            user_item=Borrower.objects.get(account=user_account)
        except:
            user_item=None
    if(0!=int(error_id)):
        try:
            error_item=Error.object.get(id=error)
        except:
            errot_item=None
    try:
        booking_item=Book.objects.get(id=book_id)
    except:
        booking_item=None

    context={
        'booking_item':booking_item,
        'user_item':user_item,
        'error_item':error_item,
    }

    return render_to_response(
        'booking.html',
        context,
        context_instance=RequestContext(request))


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