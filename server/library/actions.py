#!/usr/bin/env python
# -*- coding: utf-8 -*-
#类似views.py, 不过这是用来处理表单的
from django.shortcuts import render
from django import template
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from models import Book

def search_action(request):
    pass

def booking_action(requese):
    pass

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
                bcover=inputed_bcover,
                publisher=inputed_publisher,
                totalnum=int(inputed_insertednum),
                available=int(inputed_insertednum),
                )
            book.save()
            return HttpResponseRedirect("/success/insert")

        except Book.MultipleObjectsReturned: #isbn不唯一
            return HttpResponseRedirect("/failed/insert")

    except Exception as err:
        return HttpResponseRedirect("/failed/insert")
    

def return_action(request):
    pass

def return2_action(request):
    pass

