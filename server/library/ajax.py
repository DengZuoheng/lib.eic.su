# -*- coding: utf-8 -*-
#类似views.py, 不过这是用来处理ajax请求的

from django.shortcuts import render
from django import template
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.conf import settings
import json
import service
from models import Book
from models import Borrower
from models import BookingRecord
from models import Watcher
from models import Error
import os.path
import md5
import hashlib
import copy
import check
from server.fields import B
from server import log


def on_admin_request(request):
    #TODO: 要添加用户认证
    var={'watch_list':[]}

    try:
        watcher_list=Watcher.objects.all().exclude(account=settings.SUPER_USER)
        for item in watcher_list:
            var['watch_list'].append({
                'account':item.account,
                'name':item.name,
                'lpnumber':item.lpnumber,
                'spnumber':item.spnumber,
                'watchsum':item.watchsum,
                'iswatching':item.iswatching_str(),
                'type':'normal',
                })
        var['flag']='true'
        return HttpResponse(json.dumps(var))  

    except Exception as e:
        return HttpResponse(json.dumps({'flag':'false'}))  

def on_perinfo_request(request):
    req_account = request.POST['account']
    try:
        
        borrower=Borrower.objects.get(account=req_account)
        var = {
            'flag':'true',
            'account':borrower.account,
            'name':borrower.name,
            'lpnumber':borrower.lpnumber,
            'spnumber':borrower.spnumber,
        }

        __bookednum = BookingRecord.objects.filter(
            borrower_id=borrower.id,
            hasaccepted=True,
            hasborrowed=False).count()
        var['bookednum']=__bookednum

        if(borrower.badcredit()):
            var['badcredit']='true'
        else:
            var['badcredit']='false'

        return HttpResponse(json.dumps(var))  

    except Borrower.DoesNotExist as e:
        var = {
            'flag':'false',
            'bookednum':0,
            'badcredit':'false',
        }
        return HttpResponse(json.dumps(var)) 
    except Exception as e:
        print str(e) 
        return HttpResponse(json.dumps({'flag':'false'}))  

def on_bookinfo_request(request):
    req_isbn=request.POST['isbn']
    var={}
    
    try:
        book_list=list(Book.objects.filter(isbn=req_isbn))

        var['books']=[]
        for item in book_list:
            var['books'].append({
                'bid':item.id,
                'bname':item.bname,
                'binventory':item.bookable(),#被预约的不外借
                })

        var['flag']='true'
        return HttpResponse(json.dumps(var))
    except Exception as e:
        return HttpResponse(json.dumps({'flag':'false'}))  

def on_insert_bookinfo_request(request):
    req_isbn=request.POST['isbn']
    try:
        
        book=Book.objects.get(isbn=req_isbn)

        var ={
            'isbn':book.isbn,
            'bcover':book.bcover,
            'bname':book.bname,
            'author':book.author,
            'translator':book.translator,
            'publisher':book.publisher,
            'byear':book.byear,
            'pagination':book.pagination,
            'price':book.price,
            'totalnum':book.totalnum,
            'flag':'true'
        }
    except Book.DoesNotExist as e:
        var = service.download_book_info(isbn=req_isbn)        
        if(var['flag']!='flase'):
            var['totalnum']=0

    return HttpResponse(json.dumps(var))
    

def on_admin_push(request):
    #TODO:要求用户验证
    #前端传过来的是序列化后的json字符串, 需要loads一下
    watcher=None
    try:
        if request.session['account']!=settings.SUPER_USER:
            try:
                Watcher.objects.get(account=request.session['account'],iswatching=True)
            except:
                raise Exception(unicode("非法用户尝试修改值班干事"))
        push_json_str=request.POST['data']
        push_json=json.loads(push_json_str)
        for item in push_json['watch_list']:
            #检查输入
            log.debug('on_admin_push','for item start checking')
            keys = ['account','watchsum','name','spnumber','iswatching','lpnumber','type']
            for key in keys:
                if key not in item:
                    raise Exception('incomplete data')
                if check.is_clean_input(key,item[key]) == False:
                    print key, item[key]
                    raise Exception('unsafe data')
            log.debug('on_admin_push','for item end checking')
            #先删除
            log.debug('on_admin_push','delete items')
            if item.get('type')=='delete':
                is_logined = (item['account']==request.session['account'])
                log.debug('on_admin_push','%s deleted'%item['account'])
                Watcher.objects.all().filter(account=item['account']).delete()
                if is_logined: 
                    del request.session['account']
            else:
                if item.get('type')=='new':
                    default_password=hashlib.md5(item['account']).hexdigest()
                    default_password=hashlib.sha1(default_password).hexdigest()
                    log.debug('on_admin_push','trying to create new watcher %s'%item['account'])
                    watcher=Watcher(
                        account=B(item['account']),
                        name=B(item['name']),
                        lpnumber=B(item['lpnumber']),
                        spnumber=B(item['spnumber']),
                        password=B(default_password),
                        watchsum=0,
                        iswatching=False)
                    log.debug('on_admin_push','succeed to create new watcher')
                else:
                    log.debug('on_admin_push','trying to get item %s'%item['account'])
                    watcher=Watcher.objects.get(account=item['account'])
                    log.debug('on_admin_push','succeed to get item')
                if('yes'==item['iswatching']):
                    watcher.iswatching=True
                elif('no'==item['iswatching']):
                    watcher.iswatching=False
                    if watcher.account == request.session['account'] and watcher.account!=settings.SUPER_USER:
                        del request.session['account']
                log.info('on_admin_push','after setting watching state')
                watcher.save()
                log.info('on_admin_push','after save')
        return HttpResponse(json.dumps({'flag_succeed':'true',}))

    except Exception as e:
        log.error('exception in on_admin_push:',unicode(e))
        error=Error(what=B(unicode(e)))
        error.save()
        return HttpResponse(json.dumps({'flag_succeed':'false',}))

def on_upload_push(request):
    try:
        input_file=request.FILES['input-cover']
        filename=input_file.name
        extension = os.path.splitext(filename)[1][1:]
        import hashlib
        import datetime
        token=filename+str(datetime.datetime.now())
        new_file_name=hashlib.sha1(token).hexdigest()+'.'+extension
        
        file_url=service.img_upload_storage(input_file,new_file_name)
    except Exception as e:
        return HttpResponse(json.dumps({'error':unicode(e),}))
    return HttpResponse(json.dumps({'flag_succeed':'true','filename':filename,'file_url':file_url,}))

