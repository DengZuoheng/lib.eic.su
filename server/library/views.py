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
import json

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

def borrowing(request,book_id='0',user_account='0',booking_record_id='0',error_id='0'):
    booklist=[]
    user_item=None
    inputed_bsubc=None
    error_item=None
    booking_record=None
    #如果有书籍id,就填充书籍信息
    if(0!=int(book_id)):
        try:
            booklist=[Book.objects.get(id=book_id)]
        except:
            pass
    #如果有用户id,就填充用户信息
    if(u'0'!=user_account):
        try:
            user_item=Borrower.objects.get(account=user_account)
        except:
            pass
    #如果有预约id, 就据此填充书籍和用户信息
    if(0!=int(booking_record_id)):
        try:

            booking_record=BookingRecord.objects.get(id=booking_record_id)
            booklist=[booking_record.book]
            user_item=booking_record.borrower
        except Exception as e:
            print(str(e))
    #如果有error, 就附带错误信息
    
    if(0!=int(error_id)):
        try:
            error=Error.objects.get(id=error_id)
            data=error.json()

            inputed_bsubc=data['inputed_bsubc']

            error_item={
                'what':data['what'],
            }
        except Exception as e:
            pass

    context={
        'booklist':booklist,
        'user_item':user_item,
        'inputed_bsubc':inputed_bsubc,
        'error_item':error_item,
        'booking_record':booking_record,
        }

    return render_to_response(
            'borrowing.html',
            context,
            context_instance=RequestContext(request))

def booking(request,book_id,user_account,error_id):
    booking_item=None
    user_item=None
    error_item=None
    inputed_bsubc=None
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

def history(request,book_id='0',user_account='0',return_status='null'):
    filter_kwargs={}
    history_list=None

    if(0!=int(book_id)):
        filter_kwargs['book_id']=book_id

    if('0'!=user_account):
        filter_kwargs['borrower_id']=user_account

    if('null'!=return_status):
        if('true'==return_status):
            filter_kwargs['hasreturn']=True
        elif('false'==return_status):
            filter_kwargs['hasreturn']=False

    try:
        if(0==len(filter_kwargs)):
            history_list=list(BorrowRecord.objects.all().order_by('-btime'))
        else:
            history_list=list(BorrowRecord.objects.filter(**filter_kwargs).order_by('-btime'))

        return render_to_response('history.html',{'history_list':history_list})
    
    except Exception as e:
            print(str(e))

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

def admin(request):
    return render_to_response('admin.html',context_instance=RequestContext(request))


def return1(request,error_id='0'):
    error=None
    if(0!=int(error_id)):
        try:
            error=Error.objects.get(id=error_id)
            data=json.loads(error.what)
            error_item={'waht':data['what'],'inputed_uid':data['inputed_uid']}
        except Exception as e:
            error_item={'what':str(e),}
    context={'error_item':error_item,}
    return render_to_response('return.html',context,context_instance=RequestContext(request))

def return2(request,book_id='0',user_account='0',borrow_record_id='0',error_id='0'):
    pass