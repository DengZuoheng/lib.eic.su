#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_save

import re
import tokenizer

from library.models import Book,Error

# Create your models here.

#分词索引
class Index(models.Model):
    index=models.CharField(max_length=20,blank=True)
    books=models.ManyToManyField(Book)
    def __unicode__(self):
        return self.index

#去除中文英文字符与空白
def delzifu(text):
    return re.sub(ur'(《|》|（|）|｛|｝|【|】|！|？|、|‘|：|；|。|，|_|\s|[^\u4e00-\u9fa5\w])','',text)

#存储分词
def save_index(text,book):
    text = text.lower()#转化为小写
    text = delzifu(text)
    if text=='':
        return
    try:
        i = Index.objects.get(index=text)
        i.books.add(book)
    except Index.DoesNotExist:#先查找是否存在该分词 不存在则创建
        try:
            i = Index(index=text)
            i.save()
            i.books.add(book)
        except Exception as e:
            error=Error(what='add index:("'+text+'"")error:'+str(e))
            error.save()
    except Exception as e:
        error=Error(what='find index:("'+text+'"")error:'+str(e))
        error.save()

#存储Book时对bname和author分词
def book_post_save(sender, instance, signal, *args, **kwargs):  
    book = instance
    #判断是否二次更新书籍信息，如果是则删除原来的索引
    try:
        i=book.index_set.all()
        if i:
            i.delete()
    except Exception as e:
        error=Error(what='rebuild book index:("'+book.bname+'"")error:'+str(e))
        error.save()
    words = tokenizer.cut_for_search(book.bname)#字典分词
    for w in words:
        save_index(w,book)
    words = re.findall(ur"([\u4e00-\u9fa5]+)|(\w+)", delzifu(book.author))#取连续的中文与英文作为分词
    words.append(re.findall(ur"([\u4e00-\u9fa5]+)|(\w+)", delzifu(book.translator)))#取连续的中文与英文作为分词
    for w_ in words:
        if w_:
            if w_[0]:
                w=w_[0]
            elif w_[1]:
                w=w_[1]
            save_index(w,book)
    w = re.sub(ur'(出版社)','',delzifu(book.publisher))
    print w
    if w:
        save_index(w,book)#出版社存储不带出版社字眼分词


#Book数据库存储时触发book_post_save
post_save.connect(book_post_save, sender=Book) 
