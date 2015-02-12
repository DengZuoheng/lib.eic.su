from django.db import models
from django.db.models.signals import post_save

import jieba
import re
import json

from library.models import Book,Error

# Create your models here.

class Index(models.Model):
    index=models.CharField(max_length=20,blank=True)
    books=models.ManyToManyField(Book)
    def __unicode__(self):
        return self.index

def book_post_save(sender, instance, signal, *args, **kwargs):  
    book = instance
    words = jieba.cut_for_search(book.bname)
    for w in words:
        try:
            i = Index.objects.get(index=w)
            i.books.add(book)
        except Index.DoesNotExist:
            try:
                i = Index(index=w)
                i.save()
                i.books.add(book)
            except Exception as e:
                error=Error(what='add index:("'+w+'"")error:'+str(e))
                error.save()
        except Exception as e:
            error=Error(what='find index:("'+w+'"")error:'+str(e))
            error.save()
    words = re.findall(ur"([\u4e00-\u9fa5]+)|(\w+)", book.author)
    for w_ in words:
        if w_[0]:
            w=w_[0]
        elif w_[1]:
            w=w_[1]
        try:
            i = Index.objects.get(index=w)
            i.books.add(book)
        except Index.DoesNotExist:
            try:
                i = Index(index=w)
                i.save()
                i.books.add(book)
            except Exception as e:
                error=Error(what='add index:("'+w+'"")error:'+str(e))
                error.save()
        except Exception as e:
            error=Error(what='find index:("'+w+'"")error:'+str(e))
            error.save()

post_save.connect(book_post_save, sender=Book) 
