#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django import template
from django.shortcuts import render_to_response
from library.models import * 
from django.http import HttpResponse
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.http import  HttpResponseNotFound
from django.core.urlresolvers import reverse
import json
import service
from django.views.decorators.csrf import ensure_csrf_cookie
from server.fields import B

# Create your views here.
def collection(request):
    context={'collection':True}
    
    context['session']=Watcher.class_get_session_name(request.session)

    book_list=list(Book.objects.all().exclude(totalnum=0))
    context['book_list']=book_list
    context['total'] = len(book_list)
    return render_to_response('collection.html', context)

def order(request,book_id='0',user_account='0',error_id='0',accept_status='null',borrow_status='null'):
    #检查输入
    try:
        int(book_id)
        int(user_account)
        int(error_id)
        if accept_status not in ['null','false','true']:
            raise Exception()
        if borrow_status not in ['null','false','true']:
            raise Exception()
    except:
         return HttpResponseNotFound()
    context={'order':True}
    filter_kwargs={}
    context['session']=Watcher.class_get_session_name(request.session)
    if( context['session']==None ):
        return HttpResponseRedirect('/account/login/')
    
    error_item=None
    if(0!=int(error_id)):
        try:
            error_item=Error.objects.get(id=error_id)
        except Exception as e:
            error_item={'what':unicode(e),}
    #设置过滤条件
    if(u'0'!=user_account):
        filter_kwargs['borrower_id']=user_account
        
    if(0!=int(book_id)):
        filter_kwargs['book_id']=book_id
        
    if(r'null'!=accept_status):
        if(r'false'==accept_status):
            filter_kwargs['hasaccepted']=False
        elif(r'true'==accept_status):
            filter_kwargs['hasaccepted']=True
    
    if(r'null'!=borrow_status):
        if(r'false'==borrow_status):
            filter_kwargs['hasborrowed']=False
        elif(r'true'==borrow_status):
            filter_kwargs['hasborrowed']=True
    
    #设置前端导航栏的高亮
    if(accept_status=='null' and borrow_status=='false'):
        context['order_noncomplete']=True
    elif(accept_status=='false' and borrow_status=='null'):
        context['order_nonaccept']=True
    elif(accept_status=='true' and borrow_status=='false'):
        context['order_nonborrow']=True

    #执行查询
    if(0==len(filter_kwargs)):
        context['order_all']=True
        order_list=list(BookingRecord.objects.all().order_by('-btime'))
    else:
        order_list=list(BookingRecord.objects.filter(**filter_kwargs).order_by('-btime'))
    
    context['order_list']=order_list
    context['error_item']=error_item
    return render_to_response('order.html',context)

def borrowing(request,book_id='0',user_account='0',booking_record_id='0',error_id='0'):
    #检查输入
    try:
        int(book_id)
        int(user_account)
        int(booking_record_id)
        int(error_id)
    except:
        return HttpResponseNotFound()

    booklist=[]
    user_item=None
    inputed_bsubc=None
    error_item=None
    booking_record=None
    session=Watcher.class_get_session_name(request.session)
    if( session==None ):
        return HttpResponseRedirect('/account/login/')
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
            print(unicode(e))
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
        'borrowing':True,
        'session':session,
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
    #检查输入
    try:
        int(book_id)
        int(user_account)
        int(error_id)
    except:
        return HttpResponseNotFound()

    booking_item=None
    user_item=None
    error_item=None
    inputed_bsubc=None
    #user_account和error_id都可以是0, 但是book_id必须有效
    session=Watcher.class_get_session_name(request.session)
    if( session==None ):
        pass

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
        error_item={'what':Book.STATIC_BOOK_NOT_FIND}
        booking_item=None

    context={
        'booking':True,
        'session':session,
        'booking_item':booking_item,
        'user_item':user_item,
        'error_item':error_item,
    }
    return render_to_response(
        'booking.html',
        context,
        context_instance=RequestContext(request))


def subject(request,book_id):
    #检查输入
    try:
        int(book_id)
    except:
        return HttpResponseNotFound()
    session=Watcher.class_get_session_name(request.session)
    if( session==None ):
        pass
    book=Book.objects.get(id=book_id)
    context={
        'session':session,
        'book':book,
    }
    return render_to_response('subject.html',context)

def history(request,book_id='0',user_account='0',return_status='null'):
    #检查输入:
    try:
        int(book_id)
        int(user_account)
        if return_status not in ['null','true','false']:
            raise Exception()
    except:
        return HttpResponseNotFound()

    filter_kwargs={}
    history_list=None
    session=Watcher.class_get_session_name(request.session)
    context={}
    if( session==None ):
        return HttpResponseRedirect('/account/login/')
    if(0!=int(book_id)):
        filter_kwargs['book_id']=book_id

    if('0'!=user_account):
        try:
            borrower = Borrower.objects.get(account=user_account)
            filter_kwargs['borrower_id']=borrower.id
        except:
            filter_kwargs['borrower_id']=0

    if('null'!=return_status):
        if('true'==return_status):
            filter_kwargs['hasreturn']=True
            context['history_hasreturn']=True
        elif('false'==return_status):
            filter_kwargs['hasreturn']=False
            context['history_nonreturn']=True
    else:
        context['history_all']=True

    try:
        if(0==len(filter_kwargs)):
            history_list=list(BorrowRecord.objects.all().order_by('-btime'))
        else:
            history_list=list(BorrowRecord.objects.filter(**filter_kwargs).order_by('-btime'))
        context.update({
            'history':True,
            'session':session,
            'history_list':history_list,
        })
        return render_to_response('history.html',context)
    
    except Exception as e:
            print(unicode(e))

def index(request):
    session=Watcher.class_get_session_name(request.session)
    context={
        'session':session,
    }
    print(unicode(context))
    return  render_to_response('index.html',context,context_instance=RequestContext(request))

def insert(request,error_id='0'):
    try:
        int(error_id)
    except:
        return HttpResponseNotFound()
    context={'insert':True,}
    session=Watcher.class_get_session_name(request.session)
    if( session==None ):
        return HttpResponseRedirect('/account/login/')
    context['session']=session

    if(0!=int(error_id)):
        try:
            error=Error.objects.get(id=error_id)
            data=json.loads(error.what)          
            context['error_item']=data

        except Exception as e:
            print(unicode(e))

    return  render_to_response('insert.html',context,context_instance=RequestContext(request))

def success(request,type,extra_param='0'):
    try:
        int(extra_param)
    except:
        return HttpResponseNotFound()
    success_dict={
        'booking':False,
        'return':False,
        'borrow':False,
        'admin':False,
        'insert':False,
        'back_href':'/index/',
        'github':'https://github.com/DengZuoheng/lib.eic.su/issues'
    }
    session=Watcher.class_get_session_name(request.session)
    if( session==None ):
        pass

    if(type=='insert'):
        success_dict['back_href']='/insert/'
        success_dict['insert']=True
    elif(type=='admin'):
        success_dict['back_href']='/admin/'
        success_dict['admin']=True
    elif(type=='borrow'):
        try:
            borrower=Borrower.objects.get(account=extra_param)
            success_dict['borrower']=borrower
        except:
            pass
        success_dict['back_href']='/borrow/'
        success_dict['borrow']=True
    elif(type=='return'):
        try:
            borrower=Borrower.objects.get(account=extra_param)
            success_dict['borrower']=borrower
        except:
            pass
        success_dict['back_href']='/return/'
        success_dict['return']=True
    elif(type=='booking'):
        try:
            success_dict['booking']=True
            success_dict['watcher']=Watcher.class_get_current_watcher()
        except:
            success_dict['watcher']={
                'name':Watcher.STATIC_HAS_NO_WATCHER,
                'spnumber':'',
                'lpnumber':'',
            }
            
    context={
        'session':session,
        'success':success_dict,
    }
    return render_to_response('success.html',context)

def accept_booking(request,book_id='0',user_account='0',brid='0'):
    #检查输入
    try:
        int(book_id)
        int(user_account)
        int(brid)
    except:
        return HttpResponseNotFound()
    try:
        booking_record=BookingRecord.objects.get(id=brid);
        booking_record.hasaccepted=True
        
        booking_record.save()
        return HttpResponseRedirect(reverse('library.views.order', args=[0,0,0,'null','false']))
    except Exception as e:
        error=Error(what=B(unicode(e)))
        error.save()
        return HttpResponseRedirect(reverse('library.views.order', args=[book_id,user_account,error.id,'null','false']))

def cancel_booking(request,book_id='0',user_account='0',brid='0'):
    try:
        int(book_id)
        int(user_account)
        int(brid)
    except:
        return HttpResponseNotFound()

    try:
        booking_record=BookingRecord.objects.get(id=brid)
        
        booking_record.delete()
        return HttpResponseRedirect(reverse('library.views.order', args=[book_id,user_account,0,'null','null']))
    except Exception as e:
        error=Error(what=B(unicode(e)))
        error.save()
        return HttpResponseRedirect(reverse('library.views.order', args=[book_id,user_account,error.id,'null','null']))

def admin(request):
    session=Watcher.class_get_session_name(request.session)
    if( session==None ):
        return HttpResponseRedirect('/account/login/')
    context={
        'session':session,
        'admin':True,
    }
    return render_to_response('admin.html',context,context_instance=RequestContext(request))


def return1(request,error_id='0'):
    try:
        int(error_id)
    except:
        return HttpResponseNotFound()
    session=Watcher.class_get_session_name(request.session)
    if( session==None ):
        return HttpResponseRedirect('/account/login/')
    error=None
    error_item=None
    if(0!=int(error_id)):
        try:
            error=Error.objects.get(id=error_id)
            data=json.loads(error.what)
            error_item={'waht':data['what'],'inputed_uid':data['inputed_uid'],}
        except Exception as e:
            error_item={'what':unicode(e),}
    context={
        'error_item':error_item,
        'session':session,
        'return':True,
    }
    return render_to_response('return.html',context,context_instance=RequestContext(request))

def return2(request,book_id='0',user_account='0',borrow_record_id='0',error_id='0'):
    try:
        int(book_id)
        int(user_account)
        int(borrow_record_id)
        int(error_id)
    except:
        return HttpResponseNotFound()
    borrow_record=None
    error_item={}
    session=Watcher.class_get_session_name(request.session)
    if( session==None ):
        return HttpResponseRedirect('/account/login/')
    try:
        try:
            borrow_record=BorrowRecord.objects.get(id=borrow_record_id)

            if(int(book_id)!=int(borrow_record.book_id)):
                raise Exception(BorrowRecord.STATIC_INCONSISTENT_ID)
            if(int(user_account)!=int(borrow_record.borrower_id)):
                print 'ue'
                raise Exception(BorrowRecord.STATIC_INCONSISTENT_ACCOUNT)

        except Exception as e:
            raise Exception(BorrowRecord.STATIC_BAD_BORROWRECORD+unicode(e))

        if(0!=int(error_id)):
            try:
                error=Error.objects.get(id=error_id)
                data=json.loads(error.what)
                error_item['what']=data['what']
                try:
                    error_item['inputed_status']=data['inputed_status']
                except Exception as e:
                    raise Exception(BorrowRecord.STATIC_CANNOT_GET_STATUS+unicode(e))

            except Exception as e:
                try:
                    error_item['what']=error_item['what']+unicode(e)
                except:
                    error_item['what']=unicode(e)
        print(error_item)
        context={
            'record':borrow_record,
            'error_item':error_item,
            'return':True,
            'session':session,
        }
        return render_to_response('returns2.html',context,context_instance=RequestContext(request))
    except Exception as e:
        print(unicode(e))


def upload(request):
    context={"upload":True}
    session=Watcher.class_get_session_name(request.session)
    context['session']=session
    return render_to_response('upload.html',context,context_instance=RequestContext(request))

def help(request):
    context={"help":True}
    session=Watcher.class_get_session_name(request.session)
    context['session']=session
    context['watcher_item']=Watcher.class_get_current_watcher()
    return render_to_response('help.html',context)