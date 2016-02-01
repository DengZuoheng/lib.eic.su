#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
import types
from django.db.models.signals import post_save

import re
import tokenizer

from library.models import Book,Error
from server.fields import B

# Create your models here.

#分词索引
class Index(models.Model):
    index=models.CharField(max_length=120,blank=True,unique=True)
    books=models.ManyToManyField(Book)
    def __unicode__(self):
        return self.index

#去除标点符号
def remove_punctuation(text):
    return re.sub(ur'(《|》|（|）|｛|｝|【|】|！|？|、|‘|：|；|。|，|_|\s|[^\u4e00-\u9fa5\w])','',text)

#存储分词
def save_index(text,book):
    text = text.lower()#转化为小写
    text = remove_punctuation(text)
    if not text:
        return
    if not book:
        return
    try:
        i, _ = Index.objects.get_or_create(index=text.encode('utf-8'))
        i.books.add(book)
        i.save()
    except Exception as e:
        print str(e)

def indexing_by_words(book,words):
    if not words:
        return
    if isinstance(words,str) or isinstance(words,unicode):
        save_index(words,book)
    else:
        if hasattr(words, '__iter__') or isinstance(words, types.GeneratorType):
            for item in words:
                indexing_by_words(book,item)

def indexing_by_sentence(book,sentence):
    sentence = remove_punctuation(sentence)
    if not sentence:
        return
    words = tokenizer.segment(sentence)
    indexing_by_words(book,words)

def index_book(book):
    #判断是否二次更新书籍信息，如果是则删除原来的索引
    try:
        all_index = book.index_set.all()
        if all_index:
            all_index.delete()
    except Exception as e:
        err = 'failed to rebuild index of "%s" because:%s'%(book.isbn,str(e))
        error = Error(what=B(err))
        error.save()
    #开始分词
    indexing_by_sentence(book,book.bname)#对书名建立索引
    indexing_by_words(book,book.bname)
    indexing_by_sentence(book,book.author)#对作者建立索引
    indexing_by_sentence(book,book.translator)#对翻译者建立索引
    indexing_by_sentence(book,book.publisher)#对出版社建立索引
    indexing_by_words(book,book.publisher)
    indexing_by_words(book,book.isbn)#对isbn建立索引


#存储Book时对bname和author分词
def book_post_save(sender, instance, signal, *args, **kwargs):  
    book = instance
    try:
        return index_book(book)
    except:
        pass
   
#Book数据库存储时触发book_post_save
post_save.connect(book_post_save, sender=Book) 
