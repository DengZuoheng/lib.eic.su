#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
邓作恒
dengzuoheng@gmail.com
2015/1/30
"""
from django.db import models
import datetime

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
        return len(BookingRecord.objects.all().filter(
                hasborrowed=False,bid=self.id))

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

"""
值班人员表
"""
class Watcher(models.Model):
    password = models.CharField(max_length=128)
    iswatching = models.BooleanField(default=False)
    watchsum = models.IntegerField()

"""
外借记录表
"""
class BorrowRecord(models.Model):
    book = models.ForeignKey(Book)
    borrower = models.ForeignKey(Borrower,related_name='+')
    btime = models.DateTimeField() #借书时间
    rtime = models.DateTimeField() #还书时间
    bsubc = models.TextField() #借书时书的状态, 用text描述
    #还书时的状态{正常:normal,预期:overdue,损坏:damaged,遗失:lost}
    rsubc = models.CharField(max_length=12) 
    hasreturn = models.BooleanField(default=False)
    boperator = models.ForeignKey(Watcher,related_name='+')
    roperator = models.ForeignKey(Watcher,related_name='+')
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
    book = models.ForeignKey(Book)
    borrower = models.ForeignKey(Borrower)
    bnum = models.IntegerField()#预约的数量
    btime = models.DateTimeField()#产生预约的时间
    hasaccepted = models.BooleanField(default=False)
    hasborrowed = models.BooleanField(default=False)
    def btime_str(self):
        return self.btime.strftime("%y/%m/%d %H:%M")
    def accept_href(self):
        return "/accept/"+str(self.id)
    def cancel_href(self):
        return "/cancel/"+str(self.id)
    def borrow_herf(self):
        return "/borrowing/"+str(self.id)







