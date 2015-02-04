#!/usr/bin/env python
# -*- coding: utf-8 -*-
#类似views.py, 不过这是用来处理表单的
from django.shortcuts import render
from django import template
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from models import Book
from models import Borrower
from models import BookingRecord
from models import Error
import datetime
from django.template import RequestContext
from django.core.urlresolvers import reverse

def search_action(request):
    pass

def booking_action(request,book_id):
    inputed_account=request.POST['br-input-uid']
    inputed_name=request.POST['br-input-una']
    inputed_spnumber=request.POST['br-input-usp']
    inputed_lpnumber=request.POST['br-input-ulp']
    inputed_bnum=int(request.POST['br-input-bnum'])

    try:
        borrower=Borrower.objects.get(account=inputed_account)
    except Borrower.DoesNotExist:
        borrower=Borrower(
            account=inputed_account,
            credit=12,
            name=inputed_name,
            lpnumber=inputed_lpnumber)

    #更新借书者信息
    borrower.lpnumber=inputed_lpnumber
    borrower.name=inputed_name
    if(inputed_spnumber!=''):
        borrower.spnumber=inputed_spnumber

    #先保存借书者信息, 然后在处理预约问题
    borrower.save()
    try:
        __bookednum = BookingRecord.objects.filter(
                borrower_id=borrower.account,
                hasaccepted=True,
                hasborrowed=False).count()
    except:
        __bookednum = 0
    try:
        __borrowednum=BorowerRecord.objects.filter(
            borrower_id=borrower.account,
            hasreturn=False).count()
    except:
        __borrowednum = 0

    if (inputed_bnum+__bookednum+__borrowednum>=12):
        #超过额定数量
        raise Exception(u'预约数量超过预约者的额度')

    #这里没有明显加锁, 同步问题怎么解决?
    try:
        book=Book.objects.get(id=book_id)
        booking_record=BookingRecord(
            book=book,
            borrower=borrower,
            bnum=inputed_bnum,
            btime=datetime.datetime.now(),
            hasaccepted=False,
            hasborrowed=False,
        )
        #检查还够不够数量
        if(book.bookable()>=inputed_bnum):
            book.available=book.available-inputed_bnum
            #TODO: 测试这里能不能工作
            raise Exception(u'错误猜测')
            book.save()
            booking_record.save()
            
            return HttpResponseRedirect("/success/booking")
        else:
            raise Exception(u'该书库存量小于预约数量')
            
    #有错就返回表单页面
    except Exception as e:
        
        error=Error(str(e))
        error.save()
        return HttpResponseRedirect(reverse('library.views.booking', args=[book_id,inputed_account,error.id]))
        

def borrow_action(request):
    pass

def insert_action(request):
    try:

        inputed_isbn = request.POST['br-input-isbn']
        inputed_bcover = request.POST['br-input-bcover']
        inputed_bname = request.POST['br-input-bname']
        inputed_author = request.POST['br-input-author']
        inputed_translator = request.POST['br-input-translator']
        inputed_publisher = request.POST['br-input-publisher']
        inputed_byear = request.POST['br-input-byear']
        inputed_pagination = request.POST['br-input-pagination']
        inputed_price = request.POST['br-input-price']
        inputed_insertednum = request.POST['br-input-insertednum']

        try:
            book=Book.objects.get(isbn=inputed_isbn)

            book.bname=inputed_bname
            book.author=inputed_author
            book.translator=inputed_translator
            book.byear=inputed_byear
            book.pagination=int(inputed_pagination)
            book.price=float(inputed_price)
            # TODO : 封面应该下载到本地储存或SAE storage
            book.bcover=inputed_bcover
            book.publisher=inputed_publisher
            book.totalnum=book.totalnum+int(inputed_insertednum)
            book.available=book.available+int(inputed_insertednum)

            book.save()

            return HttpResponseRedirect("/success/insert")

        except Book.DoesNotExist:
            book=Book(
                isbn=inputed_isbn,
                bname=inputed_bname,
                author=inputed_author,
                translator=inputed_translator,
                byear=inputed_byear,
                pagination=int(inputed_pagination),
                price=float(inputed_price),
                # TODO : 封面应该下载到本地储存或SAE storage
                bcover=inputed_bcover,
                publisher=inputed_publisher,
                totalnum=int(inputed_insertednum),
                available=int(inputed_insertednum),
                )
            book.save()
            return HttpResponseRedirect("/success/insert")
            #TODO:错误应该返回原来的页面
        except Book.MultipleObjectsReturned: #isbn不唯一
            return HttpResponseRedirect("/failed/insert")

    except Exception as err:
        return HttpResponseRedirect("/failed/insert")
    

def return_action(request):
    pass

def return2_action(request):
    pass

