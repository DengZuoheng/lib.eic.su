#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
邓作恒
dengzuoheng@gmail.com
2015/1/30
"""
from django.db import models

# Create your models here.
#blank=True表示该属性可以为NULL
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
    totalnum = models.IntegerField()
    available = models.IntegerField()
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

    #可预约等于在馆数减去预约但未外借的数量
    def bookable(self):
        booking_record=len(BookingRecord.objects.all().filter(
                hasborrowed=False,bid=self.id))
        return self.available - booking_record

    #预约地址
    def href(self):
        return "/booking/"+str(self.id)

    #详情地址
    def subject(self):
        return "/subject/"+str(self.id)

    #可预约的范围
    def selectable_range(self):
        return range(self.bookable())

class AbstractUser(models.Model):
    account = models.CharField(max_length=10,unique=True,primary_key=True)
    name = models.CharField(max_length=12)
    lpnumber=models.CharField(max_length=12)
    spnumber=models.CharField(max_length=6,blank=True)
    class Meta:
        abstract = True

class Borrower(AbstractUser):
    credit=models.IntegerField()

class Watcher(models.Model):
    password = models.CharField(max_length=128)
    iswatching = models.BooleanField(default=False)
    watchsum = models.IntegerField()

class BorrowRecord(models.Model):
    book = models.ForeignKey(Book)
    borrower = models.ForeignKey(Borrower,related_name='+')
    btime = models.DateField() #借书时间
    rtime = models.DateField() #还书时间
    rsubc = models.TextField() #借书时书的状态, 用text描述
    bsubc = models.IntegerField() #还书时的状态, 只用int描述,因为这是一个状态
    hasreturn = models.BooleanField(default=False)
    boperator = models.ForeignKey(Watcher,related_name='+')
    roperator = models.ForeignKey(Watcher,related_name='+')

class BookingRecord(models.Model):
    bid = models.ForeignKey(Book)
    uid = models.ForeignKey(Borrower)
    bnum = models.IntegerField()
    bdate = models.DateField()
    hasaccepted = models.BooleanField(default=False)
    hasborrowed = models.BooleanField(default=False)







