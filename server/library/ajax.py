#!/usr/bin/env python
# -*- coding: utf-8 -*-
#类似views.py, 不过这是用来处理ajax请求的

from django.shortcuts import render
from django import template
from django.shortcuts import render_to_response
from django.http import HttpResponse
import json
import service
from models import Book
from models import Borrower
from models import BookingRecord
from models import Watcher

def on_admin_request(request):
    #TODO: 要添加用户认证
    var={'watch_list':[]}

    try:
        watcher_list=Watcher.objects.all()
        for item in watcher_list:
            var['watch_list'].append({
                'account':item.account,
                'name':item.name,
                'lpnumber':item.lpnumber,
                'spnumber':item.spnumber,
                'watchsum':item.watchsum,
                'iswatching':item.iswatching_str(),
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
            borrower_id=borrower.account,
            hasaccepted=True,
            hasborrowed=False).count()
        var['bookednum']=__bookednum

        if(borrower.badcredit()):
            var['badcredit']='true'
        else:
            var['badcredit']='false'

        return HttpResponse(json.dumps(var))  

    except Borrower.DoesNotExist as e:
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
                'binventory':item.available,
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
        push_json_str=request.POST['data']
        push_json=json.loads(push_json_str)
        #其实, 每次都必须删掉所有Watcher记录,然后重建
        Watcher.objects.all().delete()
        for item in push_json['watch_list']:
            
            watcher=Watcher(
                account=item['account'],
                name=item['name'],
                lpnumber=item['lpnumber'],
                spnumber=item['spnumber'],
                #TODO:这里的密码还需要改
                password=item['account'],
                watchsum=0,
                iswatching=False)   

            if('yes'==item['iswatching']):
                watcher.iswatching=True

            elif('no'==item['iswatching']):
                watcher.iswatching=False
            else:
                pass
            
            watcher.save()

        return HttpResponse(json.dumps({'flag_succeed':'true',}))

    except Exception as e:
        print(str(e))
        return HttpResponse(json.dumps({'flag_succeed':'false',}))

