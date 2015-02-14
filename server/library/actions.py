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
from models import BorrowRecord
from models import Watcher
import datetime
import json
from django.template import RequestContext
from django.core.urlresolvers import reverse

def search_action(request):
    try:
        key_word=request.GET['search-key-word']
        return HttpResponseRedirect(reverse('library.views.search', args=[1,key_word,]))
    except Exception as e:
        print(str(e))
        return HttpResponseRedirect(reverse('library.views.index'))     

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
            name=inputed_name,
            lpnumber=inputed_lpnumber)

    #更新借书者信息
    borrower.lpnumber=inputed_lpnumber
    borrower.name=inputed_name
    if(inputed_spnumber!=''):
        borrower.spnumber=inputed_spnumber

    #先保存借书者信息, 然后在处理预约问题
    borrower.save()

    if(borrower.badcredit()):
        raise Exception(Borrower.STATIC_BAD_CREDIT_WANING)

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

    if (inputed_bnum+__bookednum+__borrowednum>=Borrower.STATIC_MAX_BORROWABLE_NUM):
        #超过额定数量
        print(inputed_bnum)
        print(__bookednum)
        print(__borrowednum)
        print(Borrower.STATIC_MAX_BORROWABLE_NUM)
        raise Exception(BookingRecord.STATIC_OUT_OF_BOOKINGABLE_RANGE)

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
            #book.available=book.available-inputed_bnum
            
            booking_record.save()
            book.save()
            
            return HttpResponseRedirect("/success/booking")
        else:
            raise Exception(BookingRecord.STATIC_AVAILABLE_LESS_THAN_BOOKNUM)
            
    #有错就返回表单页面
    except Exception as e:
       
        error=Error(what=str(e))
        error.save()
        return HttpResponseRedirect(reverse('library.views.booking', args=[book_id,inputed_account,error.id]))
        

def borrow_action(request):
    try:
        inputed_account=request.POST['br-input-uid']
        inputed_name=request.POST['br-input-una']
        inputed_spnumber=request.POST['br-input-usp']
        inputed_lpnumber=request.POST['br-input-ulp']

        inputed_isbn=request.POST['br-input-isbn']
        #因为前端是让用户选书名的, 而书名是用id作为value的
        #所以bname实际上是id
        inputed_book_id=int(request.POST['br-input-bname'])
        inputed_bnum=int(request.POST['br-input-bnum'])
        inputed_booking_record_id=0
        inputed_bsubc=request.POST['br-input-bsubc']
        #接下来看一下有没有booking_record的字段
        try:
            inputed_booking_record_id=request.POST['booking-record-token']
        except:
            pass
        
        #开始处理
        #首先处理借书人信息
        try:
            borrower=Borrower.objects.get(account=inputed_account)
            #短号可能为空
            if(''!=inputed_spnumber):
                borrower.spnumber=inputed_spnumber
            
            borrower.lpnumber=inputed_lpnumber
            borrower.name=inputed_name
            #TODO:借书人信用度的问题还没考虑
            borrower.save()

        except:
            try:
                #新建一个borrower
                borrower=Borrower(
                    account=inputed_account,
                    name=inputed_name,
                    lpnumber=inputed_lpnumber,
                    spnumber=inputed_spnumber,
                    credit=12,)
                borrower.save()
            except Exception as e:
                raise Exception(Borrower.STATIC_BAD_BORROWER_INFO+str(e))
        if(borrower.badcredit()):
            raise Exception(Borrower.STATIC_BAD_CREDIT_WANING)
        
        #然后处理书籍信息
        try:
            book=Book.objects.get(id=inputed_book_id)
        except Exception as e:
            raise Exception(Book.STATIC_BOOK_NOT_FIND+str(e))

        #然后获取值班人信息
        #try:
        #    current_watcher=Watcher.class_get_current_watcher()
        #except Exception as e:
        #    raise Exception(Watcher.STATIC_INVILID_WATCHER_INFO+str(e))

        #检查是否超过额度
        try:
            __borrowednum=BorowerRecord.objects.filter(
            borrower_id=borrower.account,
            hasreturn=False).count()
        except:
            __borrowednum = 0

        if (inputed_bnum+__borrowednum>=Borrower.STATIC_MAX_BORROWABLE_NUM):
            #超过额定数量
            raise Exception(BorrwowRecord.STATIC_OUT_OF_BORROWABLE_RANGE)


        #产生多个借书记录
        for i in range(inputed_bnum):
            BorrowRecord.objects.create(
                book=book,
                borrower=borrower,
                btime=datetime.datetime.now(),
                bsubc=inputed_bsubc,
                #boperator=current_watcher,
                #roperator=current_watcher,
                #这里用当前值班人员做还书操作者只是权宜之计
                #应该认为, roperator在和hasreturn为False时是无效的
                )
            #每个借书记录只借1本书
            book.available=book.available-1
            book.save()

        #然后看一下是不是booking_record产生的外借
        if(0!=inputed_booking_record_id):
            try:
                booking_record=BookingRecord.objects.get(id=inputed_booking_record_id)
                booking_record.hasborrowed=True
                booking_record.save()
            except Exception as e:
                raise Exception(BookingRecord.STATIC_BOOKINGRECORD_NOT_FIND+str(e))

        return HttpResponseRedirect("/success/borrow/"+borrower.account)

    except Exception as e:
       
        data={
            'inputed_bsubc':inputed_bsubc,
            'what':str(e),
        }

        error=Error(what=json.dumps(data))
        error.save()
        args=[
                inputed_book_id,
                inputed_account,
                inputed_booking_record_id,
                error.id,
            ]
        print(str(args))
        return HttpResponseRedirect(reverse('library.views.borrowing', args=args))



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
                pagination = 0,
                price=float(inputed_price),
                # TODO : 封面应该下载到本地储存或SAE storage
                bcover=inputed_bcover,
                publisher=inputed_publisher,
                totalnum=int(inputed_insertednum),
                available=int(inputed_insertednum),
                )
            if(inputed_pagination!=''):
                book.pagination=int(inputed_pagination)

            book.save()
            return HttpResponseRedirect("/success/insert")
        except Book.MultipleObjectsReturned as e: #isbn不唯一
            #TODO:其实这里新建一条记录可能比较好
            raise Exception(Book.STATIC_BOOKS_WITH_SAME_ISBN+str(e))

    except Exception as err:
        error_item={
            "inputed_isbn":inputed_isbn,
            "inputed_bcover":inputed_bcover,
            "inputed_bname":inputed_bname,
            "inputed_author":inputed_author,
            "inputed_translator":inputed_translator,
            "inputed_publisher":inputed_publisher,
            "inputed_byear":inputed_byear,
            "inputed_pagination":inputed_pagination,
            "inputed_price":inputed_price,
            "inputed_insertednum":inputed_insertednum,
            "what":str(err),
        }
        error=Error(what=json.dumps(error_item))
        error.save()
        return HttpResponseRedirect(reverse('library.views.insert', args=[error.id]))
    

def return1_action(request):
    user_account=None
    try:
        user_account=request.POST['rt-input-uid']
        return HttpResponseRedirect(reverse('library.views.history', args=[0,user_account,'false']))
    except Exception as e:
        what={
            'inputed_uid':user_account,
            'what':str(e),
        }
        error=Error(what=json.dumps(what))
        error.save()
        return HttpResponseRedirect(reverse('library.views.return1', args=[error.id]))

def return2_action(request):
    try:
        borrow_record_token=request.POST['borrow-record-token']
        book_token=request.POST['book-token']
        borrower_token=request.POST['borrower-token']
        inputed_status=request.POST['rt-input-status']
        current_watcher=Watcher.class_get_current_watcher()
        #首先获取借书记录
        try:
            borrow_record=BorrowRecord.objects.get(id=borrow_record_token)
            
        except Exception as e:
            raise Exception(BorrowRecord.STATIC_BAD_BORROWRECORD+str(e))

        #然后获取值班人信息
        try:
            current_watcher=Watcher.class_get_current_watcher()
        except Exception as e:
            raise Exception(Watcher.STATIC_INVILID_WATCHER_INFO+str(e))

        #然后视情况改变借书者的信用情况和库存情况
        if(inputed_status=='overdue'):
            
            borrow_record.borrower.credit_overdue()

        if(inputed_status=='damaged'):
            borrow_record.borrower.credit_damaged()

        if(inputed_status=='lost'):
            #丢失了应该是只减总数
            borrow_record.book.totalnum=borrow_record.book.totalnum-1
            borrow_record.borrower.credit_lost()
        else:
            borrow_record.book.available+=1
            
        #保存借书记录信息
        borrow_record.rtime=datetime.datetime.now()
        borrow_record.rsubc=inputed_status
        borrow_record.roperator=current_watcher
        borrow_record.hasreturn=True
        borrow_record.book.save()
        borrow_record.borrower.save()
        borrow_record.save()

        return HttpResponseRedirect("/success/return/"+borrow_record.borrower.account)
    except Exception as e:
        
        data={
            'inputed_status':inputed_status,
            'what':str(e),
        }

        error=Error(what=json.dumps(data))
        error.save()
        args=[
                book_token,
                borrower_token,
                borrow_record_token,
                error.id,
            ]
        print(str(args))
        return HttpResponseRedirect(reverse('library.views.return2', args=args))


