#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django import template
from django.shortcuts import render_to_response
from library.models import * 
from django.http import HttpResponse
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

# Create your views here.
def collection(request):
    book_list=list(Book.objects.all())
    return render_to_response('collection.html', {'book_list': book_list})

def order(reuqest,book_id,user_account,error_id):
    order_list=list(BookingRecord.objects.all().order_by('-btime'))
    error_item=None
    if(0!=int(error_id)):
        try:
            error_item=Error.objects.get(id=error_id)
        except Exception as e:
            error_item={'what':str(e),}
    if(u'0'!=user_account):
        try:
            order_list=list(
                BookingRecord.objects.filter(borrower_id=user_account).order_by('-btime'))
        except Exception as e:
            print(str(e))
            order_list=None
    if(0!=int(book_id)):
        try:
            order_list=list(
                BookingRecord.objects.filter(book_id=book_id).order_by('-btime'))
        except:
            order_list=None        
    
    return render_to_response('order.html',{'order_list':order_list,'error_item':error_item})

def borrowing(reuqesst):
    pass

def booking(request,book_id,user_account,error_id):
    booking_item=None
    user_item=None
    error_item=None
    
    #user_account和error_id都可以是0, 但是book_id必须有效

    if(u'0'!=user_account):
        try:
            user_item=Borrower.objects.get(account=user_account)     
        except Exception as err:
            user_item=None

    if(0!=int(error_id)):
        try: 
            error_item=Error.objects.get(id=error_id)
        except Exception as err:
            errot_item=None
    try:
        booking_item=Book.objects.get(id=book_id)
    except:
        error_item={'what':'书籍不存在'}
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

def accept_booking(request,book_id='0',user_account='0',brid='0'):
    try:
        booking_record=BookingRecord.objects.get(id=brid);
        booking_record.hasaccepted=True
        booking_record.save()
        return HttpResponseRedirect(reverse('library.views.order', args=[book_id,user_account,0]))
    except Exception as e:
        error=Error(what=str(e))
        error.save()
        return HttpResponseRedirect(reverse('library.views.order', args=[book_id,user_account,error.id]))

def cancel_booking(request,book_id='0',user_account='0',brid='0'):
    try:
        booking_record=BookingRecord.objects.get(id=brid)
        book=Book.objects.get(id=booking_record.book_id)
        book.available=book.available+booking_record.bnum
        book.save()
        booking_record.delete()
        return HttpResponseRedirect(reverse('library.views.order', args=[book_id,user_account,0]))
    except Exception as e:
        error=Error(what=str(e))
        error.save()
        return HttpResponseRedirect(reverse('library.views.order', args=[book_id,user_account,error.id]))
