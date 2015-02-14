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
import hashlib

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
    byear = models.CharField(max_length=10,blank=True)
    pagination = models.IntegerField(blank=True)
    price = models.FloatField(blank=True)
    bcover = models.URLField(blank=True)
    publisher = models.CharField(max_length=30,blank=True)
    totalnum = models.IntegerField()#总册数
    available = models.IntegerField()#在馆数

    #私有成员
    __booked_num = -1

    #静态成员
    STATIC_BOOK_NOT_FIND=u'无法找到该书籍:'
    STATIC_BOOKS_WITH_SAME_ISBN=u'不同的书有相同的isbn:'




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
        if(self.__booked_num==-1):
            try:
                booked_num=0;
                book_record_list=list(BookingRecord.objects.all().filter(
                    hasborrowed=False, book_id=self.id))
                for item in book_record_list:
                    booked_num=booked_num+item.bnum

                self.__booked_num=booked_num

                return booked_num

            except Exception as err:
                return 0
        else:
            return self.__booked_num

    #可预约等于在馆数减去预约但未外借的数量
    def bookable(self):
        if self.__booked_num==-1:
            return self.available - self.booked()
        else:
            return self.available - self.__booked_num


    #预约地址
    def href(self):
        return "/booking/bid/"+str(self.id)+"/uid/0/err/0"

    #详情地址
    def subject(self):
        return "/subject/"+str(self.id)

    #可预约的范围
    def selectable_range(self):
        return range(self.bookable())

    #封面地址
    def bcover_src(self):
        return self.bcover

    def price_str(self):
        return '%.2f'%self.price

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
    credit=models.IntegerField(default=0)
    #static_max_borrowable_num是一个人最多可借和预约的数量
    #你必须当做静态常量来用
    STATIC_MAX_BORROWABLE_NUM=8
    STATIC_CREDIT_LIMIT=4
    STATIC_BAD_BORROWER_INFO=u'无法创建借书人记录, 借书人信息有误:'
    STATIC_BAD_CREDIT_WANING=u'逾期归还, 损坏, 丢失次数过多, 已取消预约和借书资格'
    def __unicode__(self):
        return {
            "account":self.account,
            "name":self.name,
            "lpnumber":self.lpnumber,
            "spnumber":self.spnumber,
            "credit":self.credit,
        }
    def badcredit(self):
        if(self.credit>=Borrower.STATIC_CREDIT_LIMIT):
            return True
        else:
            return False

    def credit_overdue(self):
        self.credit=self.credit+1

    def credit_damaged(self):
        self.credit=self.credit+1

    def credit_lost(self):
        self.credit=self.credit+1

"""
值班人员表
"""
class Watcher(AbstractUser):
    password = models.CharField(max_length=128)
    watchsum = models.IntegerField(default=0)
    iswatching = models.BooleanField(default=False)
    
    STATIC_INVILID_WATCHER_INFO=u'值班人员数据异常:'


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

    def iswatching_str(self):
        if(self.iswatching):
            return 'yes'
        else :
            return 'no'

    def watchsum_(self):
        #TODO:这里的计算方法还不明确
        return 0

    @classmethod
    def class_get_current_watcher(cls):
        try:
            return Watcher.objects.get(iswatching=True)
        except:
            lst=list(Watcher.objects.filter(iswatching=True))
            return lst[0]

    @classmethod
    def class_get_session_name(cls,session):
        if 'account' in session:
            #已登录
            try:
                account=session['account']
                watcher=Watcher.objects.get(account=account)
                #不是当前值班就不算
                if(not watcher.iswatching):
                    if(watcher.account=='root'):
                        return {'name':watcher.name}
                    else:
                        return None
                else:
                    return {'name':watcher.name}
            except:
                return None
        else:

            return None
    #创建root账户
    @classmethod
    def class_checkout_root(cls):
        try:
            watcher=Watcher.objects.get(account='root')
            return True
        except:
            #默认密码是guido大神的名字
            default_password=hashlib.md5('Guido_van_Rossum').hexdigest()
            default_password=hashlib.sha1(default_password).hexdigest()

            watcher=Watcher(
                account='root',
                name='Administrator',
                spnumber='',
                password=default_password,
                )
            watcher.save()
            return False

"""
外借记录表
"""
class BorrowRecord(models.Model):
    book = models.ForeignKey(Book)
    borrower = models.ForeignKey(Borrower,related_name='+')
    btime = models.DateTimeField(auto_now=True) #借书时间
    rtime = models.DateTimeField(blank=True,auto_now=True) #还书时间
    bsubc = models.TextField(blank=True) #借书时书的状态, 用text描述
    #还书时的状态{正常:normal,预期:overdue,损坏:damaged,遗失:lost}
    rsubc = models.CharField(max_length=12,blank=True) 
    hasreturn = models.BooleanField(default=False)
    #boperator = models.ForeignKey(
    #        Watcher,
    #        related_name='+',
    #        on_delete=models.DO_NOTHING,
    #        blank=True,
    #        null=True)
    #roperator = models.ForeignKey(
    #        Watcher,
    #        related_name='+',
    #        on_delete=models.DO_NOTHING,
    #        blank=True,
    #        null=True)

    STATIC_BAD_BORROWRECORD=u'借书记录异常:'
    STATIC_INCONSISTENT_ID=u'输入书籍ID与借书记录不一致'
    STATIC_INCONSISTENT_ACCOUNT=u'输入学号与借书记录不一致'
    STATIC_CANNOT_GET_STATUS=u'无法获得"状态":'
    STATIC_OUT_OF_BORROWABLE_RANGE=u'借书数超过借书者的限额'

    def __unicode__(self):
        return {
            "id":str(self.id),
            "book_id":str(self.book_id),
            #"borrower_id":str(self.borrower_id),
            "btime":str(self.btime),
            "rtime":str(self.rtime),
            "bsubc":str(self.bsubc),
            "rsubc":str(self.rsubc),
            "boperator_id":str(self.boperator_id),
            "roperator_id":str(self.roperator_id),
        }
    #借用时长
    def duration(self):
        if(self.hasreturn==False):
            today = datetime.datetime.now()
            delta = today.date() - self.btime.date()
        else:
            delta = self.rtime.date()-self.btime.date()
        return delta.days

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
        return "/return2/bid/"+str(self.book_id)+"/uid/"+str(self.borrower_id)+"/brrid/"+str(self.id)+"/err/0"


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

    #静态常量
    STATIC_OUT_OF_BOOKINGABLE_RANGE=u'预约数量超过预约者的额度'
    STATIC_AVAILABLE_LESS_THAN_BOOKNUM=u'该书库存量小于预约数量'
    STATIC_BOOKINGRECORD_NOT_FIND=u'预约记录不存在:'
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
        return "/accept/bid/"+str(self.book_id)+"/uid/"+str(self.borrower_id)+"/brid/"+str(self.id)

    def cancel_href(self):
        return "/cancel/bid/"+str(self.book_id)+"/uid/"+str(self.borrower_id)+"/brid/"+str(self.id)

    def borrow_href(self):
        return "/borrowing/bid/"+str(self.book_id)+"/uid/"+str(self.borrower_id)+"/brid/"+str(self.id)+"/err/0"

    def danger(self):
        if(self.hasaccepted==False and self.hasborrowed==False):
            return True
        else :
            return False
    def info(self):
        if(self.hasaccepted==True and self.hasborrowed==False):
            return True
        else:
            return False
    def success(self):
        if(self.hasaccepted==True and self.hasborrowed==True):
            return True
        else:
            return False
    def selectable_range(self):
        return range(self.bnum)

"""
错误记录表
"""
class Error(models.Model):
    what=models.TextField(blank=True)

    def json(self):
        try:
            ret=json.loads(self.what)
            return ret
        except Exception as e:
            return {'what':self.what}
    def __unicode__(self):
        return {
            'id':self.id,
            'what':self.what,
        }






