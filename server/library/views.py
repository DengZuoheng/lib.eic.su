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
import service

# Create your views here.
def collection(request):
    context={'collection':True}
    
    context['session']=Watcher.class_get_session_name(request.session)

    book_list=list(Book.objects.all().exclude(totalnum=0))
    context['book_list']=book_list
    return render_to_response('collection.html', context)

def order(reuqest,book_id,user_account,error_id):
    context={'order':True}
    context['session']=Watcher.class_get_session_name(request.session)

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
    context['order_list']=order_list
    context['error_item']=error_item
    return render_to_response('order.html',context)

def borrowing(request,book_id='0',user_account='0',booking_record_id='0',error_id='0'):
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
    booking_item=None
    user_item=None
    error_item=None
    inputed_bsubc=None
    #user_account和error_id都可以是0, 但是book_id必须有效
    session=Watcher.class_get_session_name(request.session)
    if( session==None ):
        return HttpResponseRedirect('/account/login/')

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
    session=Watcher.class_get_session_name(request.session)
    if( session==None ):
        return HttpResponseRedirect('/account/login/')
    book=Book.objects.get(id=book_id)
    context={
        'session':session,
        'book':book,
    }
    return render_to_response('subject.html',context)

def history(request,book_id='0',user_account='0',return_status='null'):
    filter_kwargs={}
    history_list=None
    session=Watcher.class_get_session_name(request.session)
    if( session==None ):
        return HttpResponseRedirect('/account/login/')
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
        context={
            'history':True,
            'session':session,
            'history_list':history_list,
        }
        return render_to_response('history.html',context)
    
    except Exception as e:
            print(str(e))

def index(request):
    session=Watcher.class_get_session_name(request.session)
    context={
        'session':session,
    }
    print(str(context))
    return  render_to_response('index.html',context,context_instance=RequestContext(request))

def insert(request,error_id='0'):
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
            print(str(e))

    return  render_to_response('insert.html',context,context_instance=RequestContext(request))

def success(request,type,extra_param='0'):
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
        return HttpResponseRedirect('/account/login/')

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

        success_dict['watcher']=Watcher.class_get_current_watcher()
        success_dict['booking']=True
    context={
        'session':session,
        'success':success_dict,
    }
    return render_to_response('success.html',context)

def accept_booking(request,book_id='0',user_account='0',brid='0'):
    try:
        booking_record=BookingRecord.objects.get(id=brid);
        booking_record.hasaccepted=True
        booking_record.save()
        return HttpResponseRedirect(reverse('library.views.order', args=[0,0,0]))
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
    session=Watcher.class_get_session_name(request.session)
    if( session==None ):
        return HttpResponseRedirect('/account/login/')
    context={
        'session':session,
        'admin':True,
    }
    return render_to_response('admin.html',context,context_instance=RequestContext(request))


def return1(request,error_id='0'):
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
            error_item={'what':str(e),}
    context={
        'error_item':error_item,
        'session':session,
        'return':True,
    }
    return render_to_response('return.html',context,context_instance=RequestContext(request))

def return2(request,book_id='0',user_account='0',borrow_record_id='0',error_id='0'):
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
            if(user_account!=borrow_record.borrower_id):
                raise Exception(BorrowRecord.STATIC_INCONSISTENT_ACCOUNT)

        except Exception as e:
            raise Exception(BorrowRecord.STATIC_BAD_BORROWRECORD+str(e))

        if(0!=int(error_id)):
            try:
                error=Error.objects.get(id=error_id)
                data=json.loads(error.what)
                error_item['what']=data['what']
                try:
                    error_item['inputed_status']=data['inputed_status']
                except Exception as e:
                    raise Exception(BorrowRecord.STATIC_CANNOT_GET_STATUS+str(e))

            except Exception as e:
                try:
                    error_item['what']=error_item['what']+str(e)
                except:
                    error_item['what']=str(e)
        print(error_item)
        context={
            'record':borrow_record,
            'error_item':error_item,
            'return':True,
            'session':session,
        }
        return render_to_response('returns2.html',context,context_instance=RequestContext(request))
    except Exception as e:
        print(str(e))

def search(request,start_idx,key_word):
    start_idx=int(start_idx)
    session=Watcher.class_get_session_name(request.session)
    book_list=service.search_by(key_word)
    result={}
    MAX_NO_PAGING=24#如果结果不超过32个,这一页显示完所有结果
    NORMAL_PAGING=12#如果结果超过32个, 这每页16个
    book_list_len=len(book_list)
    try:
        if(0==book_list_len):
            raise Exception('no result')
        result['begin_idx']=start_idx
        result['total']=book_list_len
        if(start_idx==1):
            if(book_list_len<=MAX_NO_PAGING):
                result['end_idx']=book_list_len
            else:
                result['end_idx']=start_idx+NORMAL_PAGING-1 #1+16=17, 所以应减1
        else:
            if(book_list_len<=start_idx+NORMAL_PAGING):
                result['end_idx']=book_list_len
            else:
                result['end_idx']=start_idx+NORMAL_PAGING-1

        if(book_list_len>MAX_NO_PAGING):
            result['pagination'] = True
            if(start_idx==1):
                url=u'/search/start/1/keyword/'+key_word
                result['prev_page']=url
                result['is_first_page']=True
                url=u'/search/start/17/keyword/'+key_word
                result['next_page']=url
            else:
                url=u'/search/start/'+str(start_idx-NORMAL_PAGING)+'/keyword/'+key_word
                result['prev_page']=url
                result['is_first_page']=False
                url=u'/search/start/'+str(start_idx+NORMAL_PAGING)+'/keyword/'+key_word
                result['next_page']=url
            #page bar
            result['page_href_list']=[]
            begin_idx=1
            while NORMAL_PAGING <=book_list_len:
                url=u'/search/start/'+str(begin_idx)+'/keyword/'+key_word
                result['page_href_list'].append(url)
                if(begin_idx==start_idx):
                    result['current_page']=int((begin_idx)/NORMAL_PAGING)+1
                begin_idx=begin_idx+NORMAL_PAGING
                book_list_len=book_list_len-NORMAL_PAGING

            if(book_list_len>0):
                url=u'/search/start/'+str(begin_idx)+'/keyword/'+key_word
                result['page_href_list'].append(url)
                if(begin_idx==start_idx):
                    result['current_page']=int((begin_idx)/NORMAL_PAGING)+1
                    result['is_last_page']=True
                    result['next_page']=url

            result['book_list']=book_list[(result['begin_idx']-1):(result['end_idx'])]
        else:
            result['book_list']=book_list 

        context={
            'result':result,
        }
    except:
        context={
            'result':{
                'begin_idx':0,
                'end_idx':0,
                'total':0,
            },
            'session':session,
        }

    return render_to_response('search.html',context,context_instance=RequestContext(request))