#!/usr/bin/env python
# -*- coding: utf-8 -*-

from models import *

def filldb(request):
    clear_all()
    fill_book()
    fill_borrower()
    fill_watcher()
    fill_borrow_record()
    fill_booking_record()
    return "success";

def fill_book():
    b1 = Book(
            isbn="9787544143615",
            author="顾漫",
            bname = "何以笙箫默",
            byear = "2011.1",
            pagination = 256,
            price = 25.00,
            bcover = "http://img5.douban.com/lpic/s6531687.jpg",
            publisher = "沈阳出版社",
            totalnum = 10,
            available = 10,
        )
    b1.save()

def fill_borrower():
    pass

def fill_watcher():
    pass

def fill_borrow_record():
    pass

def fill_booking_record():
    pass

def clear_all():
    clear_book()
    clear_borrower()
    clear_watcher()
    clear_borrow_record()
    clear_booking_record()

def clear_book():
    Book.objects.all().delete()

def clear_borrower():
    Borrower.objects.all().delete()

def clear_watcher():
    Watcher.objects.all().delete()

def clear_borrow_record():
    BorrowRecord.objects.all().delete()

def clear_booking_record():
    BookingRecord.objects.all().delete()
