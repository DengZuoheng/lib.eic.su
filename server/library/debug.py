#!/usr/bin/env python
# -*- coding: utf-8 -*-

from models import *
from server.fields import B
from datetime import datetime

def create_new_book(book_info):
    new_book = Book(
            available=book_info['available'],
            bcover=B(book_info['bcover']),
            isbn=B(book_info['isbn']),
            price=book_info['price'],
            translator=B(book_info['translator']),
            totalnum=book_info['totalnum'],
            publisher=B(book_info['publisher']),
            pagination=book_info['pagination'],
            author=B(book_info['author']),
            byear=B(book_info['byear']),
            bname=B(book_info['bname'])
        )
    return new_book

def create_new_br(br):
    new_br = Borrower(
            credit=br["credit"],
            account=B(br["account"]),
            name=B(br["name"]),
            spnumber=B(br["spnumber"]),
            lpnumber=B(br["lpnumber"])
        )
    return new_br

def move_book(book_list):
    ret_dict={}
    for item in book_list:
        new_book = create_new_book(item)
        new_book.save()
        ret_dict[item['id']]=new_book.id
        print 'moved book',item['id']
    return ret_dict

def move_borrower(br_list):
    ret_dict={}
    for item in br_list:
        new_br = create_new_br(item)
        new_br.save()
        ret_dict[item['account']]=new_br.id
        print 'moved borrower',item['account']
    return ret_dict

def create_new_brd(brd):
    new_brd = BookingRecord(
            hasaccepted=brd['hasaccepted'],
            hasborrowed=brd['hasborrowed'],
            bnum=brd['bnum'],
            borrower=brd['borrower'],
            btime=brd['btime'],
            book=brd['book']
        )
    return new_brd

def get_borrower(brid):
    return Borrower.objects.get(id=brid)

def get_book(bid):
    return Book.objects.get(id=bid)

def get_time(t):
    return datetime.strptime(t,BookingRecord.STATIC_DATETIME_FORMAT)

def move_booking_record(book_dict,br_dict,brd):
    for item in brd:
        item['borrower']=get_borrower(br_dict[item['borrower_id']])
        item['book']=get_book(book_dict[item['book_id']])
        item['btime']=get_time(item['btime'])
        new_booking_record = create_new_brd(item)
        new_booking_record.save()
        print 'moved bookingrecord',item['id']

def move_new_db(obj):
    old_new_book_dict = move_book(obj['book'])
    old_new_borrower_dict = move_borrower(obj['borrower'])
    move_booking_record(
        old_new_book_dict,
        old_new_borrower_dict,
        obj['bookingrecord']
        )
    move_watcher(obj['watcher'])

def move_watcher(wt):
    for item in wt:
        new_wt = Watcher(
                watchsum=item['watchsum'],
                name=B(item['name']),
                spnumber=B(item['spnumber']),
                lpnumber=B(item['lpnumber']),
                account=B(item['account']),
                password=B(item['password']),
                iswatching=item['iswatching']
            )
        new_wt.save()
        print 'moved whatcher',item['account']

def move_json_to_db():
    json_str=''
    import json
    move_new_db(json.loads(json_str))