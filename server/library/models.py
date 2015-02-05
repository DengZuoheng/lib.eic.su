#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
邓作恒
dengzuoheng@gmail.com
2015/1/30
"""
from django.db import models
import datetime
import json

# Create your models here.
#blank=True表示该属性可以为NULL
"""
书籍表
"""
class Book(models.Model):
    isbn = models.CharField(max_length=13)
    bname = models.CharField(max_length=30)
    author = models.CharField(max_length=128,blank=True)
    translator = models.CharField(max_length=128,blank=True)
    byear = models.CharField(max_length=8,blank=True)
    pagination = models.IntegerField(blank=True)
    price = models.FloatField(blank=True)
    bcover = models.URLField(blank=True)
    publisher = models.CharField(max_length=30,blank=True)
    totalnum = models.IntegerField()#总册数
    available = models.IntegerField()#在馆数
    def __unicode__(self):
        return {
            "id":self.id,
            "isbn":self.bname,
            "author":self.author,
            "translator":self.translator,
            "byear":self.byear,
            "pagination":self.pagination,
            "price":self.price,
            "bcover":self.bcover,
            "publisher":self.publisher,
            "totalnum":self.totalnum,
            "available":self.available,
        }
    #如果在馆数少于5记为危险
    def danger(self):
        if(0<int(self.available)<5):
            return True;
        else:
            return False;

    def waring(self):
        if(5<=int(self.available)<10):
            return True;
        else:
            return False;
    def info(self):

        if(int(self.available)>=10):
            return True;
        else:
            return False;

    #已经预约的数量
    def booked(self):
        #TODO:这里性能好像很不科学
        try:
            #TODO : 这里貌似有bug
            return BookingRecord.objects.all().filter(
                hasborrowed=False, book_id=self.id).count()
        except Exception as err:

            return 0

    #可预约等于在馆数减去预约但未外借的数量
    def bookable(self):
        return self.available - self.booked()


    #预约地址
    def href(self):
        return "/booking/"+str(self.id)

    #详情地址
    def subject(self):
        return "/subject/"+str(self.id)

    #可预约的范围
    def selectable_range(self):
        return range(self.bookable())

    #封面地址
    def bcover_src(self):
        return "封面地址"

"""
借书人和值班人员的基类模型
"""
class AbstractUser(models.Model):
    account = models.CharField(max_length=10,unique=True,primary_key=True)
    name = models.CharField(max_length=12)
    lpnumber=models.CharField(max_length=12)
    spnumber=models.CharField(max_length=6,blank=True)
    class Meta:
        abstract = True

"""
借书人和预约人表
"""
class Borrower(AbstractUser):
    credit=models.IntegerField()
    def __unicode__(self):
        return {
            "account":self.account,
            "name":self.name,
            "lpnumber":self.lpnumber,
            "spnumber":self.spnumber,
            "credit":self.credit,
        }
    def badcredit(self):
        if(self.credit<=0):
            return True
        else:
            return False

"""
值班人员表
"""
class Watcher(models.Model):
    password = models.CharField(max_length=128)
    iswatching = models.BooleanField(default=False)
    watchsum = models.IntegerField()
    #TODO:这里的watchsum不知道什么自增
    def __unicode__(self):
        return {
            "account":self.account,
            "name":self.name,
            "lpnumber":self.lpnumber,
            "spnumber":self.spnumber,
            "password":self.password,
            "iswatching":self.iswatching,
            "watchsum":self.watchsum,
        }

"""
外借记录表
"""
class BorrowRecord(models.Model):
    book = models.ForeignKey(Book)
    borrower = models.ForeignKey(Borrower,related_name='+')
    btime = models.DateTimeField() #借书时间
    rtime = models.DateTimeField(blank=True) #还书时间
    bsubc = models.TextField(blank=True) #借书时书的状态, 用text描述
    #还书时的状态{正常:normal,预期:overdue,损坏:damaged,遗失:lost}
    rsubc = models.CharField(max_length=12,blank=True) 
    hasreturn = models.BooleanField(default=False)
    boperator = models.ForeignKey(Watcher,related_name='+',on_delete=models.DO_NOTHING)
    roperator = models.ForeignKey(Watcher,related_name='+',on_delete=models.DO_NOTHING,blank=True)

    def __unicode__(self):
        return {
            "id":self.id,
            "book_id":self.book_id,
            "borrower_id":self.borrower_id,
            "btime":self.bitme,
            "rtime":self.rtime,
            "bsubc":self.bsubc,
            "rsubc":self.rsubc,
            "boperator_id":self.boperator_id,
            "roperator":self.roperator_id,
        }
    #借用时长
    def duration(self):
        today = datetime.date.today()
        delta = today - btime
        return delta
    def danger(self):
        if(self.hasreturn==False and self.duration()>=60):
            return True
        else :
            return False
    def warning(self):
        if(self.hasreturn==False and self.duration()>=30):
            return True
        else :
            return False
    def info(self):
        if(self.hasreturn==False and self.duration()<30):
            return True
        else :
            return False
    def btime_str(self):
        return self.btime.strftime("%y/%m/%d %H:%M")
    def return_href(self):
        return "/return2/"+str(self.id)

"""
预约记录表
"""
class BookingRecord(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE,default=None)
    borrower = models.ForeignKey(Borrower,on_delete=models.DO_NOTHING,default=None)
    bnum = models.IntegerField()#预约的数量
    btime = models.DateTimeField(blank=True,default=None)#产生预约的时间
    hasaccepted = models.BooleanField(default=False)
    hasborrowed = models.BooleanField(default=False)

    def __unicode__(self):
        return {
            "id":self.id,
            "book_id":self.book_id,
            "borrower_id":self.borrower_id,
            "bnum":self.bnum,
            "btime":self.btime,
            "hasaccepted":self.hasaccepted,
            "hasborrowed":self.hasborrowed,
        }
    def btime_str(self):
        return self.btime.strftime("%y/%m/%d %H:%M")
    def accept_href(self):
        return "/accept/"+str(self.id)
    def cancel_href(self):
        return "/cancel/"+str(self.id)
    def borrow_herf(self):
        return "/borrowing/"+str(self.id)

"""
错误记录表
"""
class Error(models.Model):
    what=models.TextField(blank=True)

    def json(self):
        try:
            ret=json.load(self.what)
            return ret
        except:
            return {'what':self.what}






