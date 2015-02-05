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

def on_admin_request(request):
    pass

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
    pass

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
    pass

