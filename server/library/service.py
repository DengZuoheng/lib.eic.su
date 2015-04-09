# -*- coding: utf-8 -*-
# service就用来封装view层觉得太长的代码吧
import urllib2
import json
import unittest
from library.models import * 
from backups.models import *

def download_book_info(isbn):
    return douban_book_api(isbn)

def douban_book_api(isbn):
    url='https://api.douban.com/v2/book/isbn/'+str(isbn)
    try:
        socket=urllib2.urlopen(url)
        json_str=socket.read()
        ret=json.loads(json_str.decode('utf-8'))
        ret_dict = {
            'flag':'true',
            'isbn':ret['isbn13'],
            'author':ret['author'],
            'bname':ret['title'],
            'byear':ret['pubdate'],
            'pagination':ret['pages'],
            'price':ret['price'],
            'bcover':ret['image'],
            'publisher':ret['publisher'],
            }
        ret_dict['byear']=ret_dict['byear'].replace(u'年','.')
        ret_dict['byear']=ret_dict['byear'].replace(u'月','.')
        ret_dict['byear']=ret_dict['byear'].replace(u'日','')
        ret_dict['byear']=ret_dict['byear'].replace(u'-','.')
        ret_dict['byear']=ret_dict['byear'].replace(u'/','.')
        ret_dict['price']=ret_dict['price'].replace(u'元','')
        ret_dict['pagination']=ret_dict['pagination'].replace(u'页','')
        ret_dict['pagination']=ret_dict['pagination'].replace(u'p','')
        ret_dict['pagination']=ret_dict['pagination'].replace(u'P','')
        print(ret_dict['price'])
        try:
            ret_dict['translator']=ret['translator']
            ret_dict['bcover']=ret['images']['large']
            return ret_dict
        except:
            return ret_dict

    except urllib2.HTTPError as e:
        return {'flag':'false','error_code':e.code}
    except Exception as e:
        return {'flag':'false','error':str(e),}

def library_thing_api(isbn):
    pass

from search.search import search
def search_by(key_word):
    #TODO: 这里需要返回搜索结果, 是一个Book对象的列表, 按相关度降序   
    return search(key_word.lower()) 
#    return search_result_example()

def search_result_example():
    return list(Book.objects.all())

def storage(input_data,file_name,domain_name):
    try:
  
        import sae.storage

        client = sae.storage.Client()
        if(client==None):
            raise Exception("null client")
        obj = sae.storage.Object(input_data)
        if(obj==None):
            raise Exception("null object")
        url = client.put(domain_name, file_name, obj) 
        return url

    except Exception as e:
        return unicode(e)

def img_upload_storage(input_file, file_name):
    return storage(input_file.read(),file_name,'images')

def db_backups_storage(input_data, file_name=''):
    if(''==file_name):
        import datetime
        now=datetime.datetime.now()
        args=(now.year,now.month,now.day,now.hour,now.minute,now.second)
        file_name="lib.eic.su.backups.%s.%s.%s.%s.%s.%s.json"%args
    try:
        return storage(input_data,file_name,'backups')
    except Exception as e:
        return unicode(e)

def get_backup_by_id(id):
    backup_record = BackupRecord.objects.get(id=id)
    import urllib2
    return (backup_record.version, urllib2.urlopen(backup_record.url))


def db_backups():
    book_list=[]
    borrower_list=[]
    watcher_list=[]
    borrowrecord_list=[]
    bookingrecord_list=[]
    book_list=Book.objects.all()
    borrower_list=Borrower.objects.all()
    watcher_list=Watcher.objects.all()
    borrowrecord_list=BorrowRecord.objects.all()
    bookingrecord_list=BookingRecord.objects.all()
    var={
        'book':[],
        'borrower':[],
        'watcher':[],
        'borrowrecord':[],
        'bookingrecord':[],
    }
    for item in book_list:
        var['book'].append(item.dict())
    for item in borrower_list:
        var['borrower'].append(item.dict())
    for item in watcher_list:
        var['watcher'].append(item.dict())
    for item in borrowrecord_list:
        var['borrowrecord'].append(item.dict())
    for item in bookingrecord_list:
        var['bookingrecord'].append(item.dict())
    
    return var

def backup_redo(json_obj):
    db_restore(json_obj)

def backup_overide(json_obj):
    Book.objects.all().delete()
    Borrower.objects.all().delete()
    Watcher.objects.all().delete()
    BorrowRecord.objects.all().delete()
    BookingRecord.objects.all().delete()
    db_restore(json_obj)

def db_restore(backup):  
    for item in backup['book']:
        restore_model(item, Book)
    for item in backup['borrower']:
        restore_model(item, Borrower)
    for item in backup['watcher']:
        restore_model(item, Watcher)
    for item in backup['borrowrecord']:
        restore_model(item, BorrowRecord)
    for item in backup['bookingrecord']:
        restore_model(item, BookingRecord)

    return True

def restore_model(data,cls):

    try:

        if(data.has_key('id')):
            item=cls.objects.get(id=int(data['id']))
            item.setattr(data)
            item.save()
        else:
            item=cls.objects.get(account=data['account'])
            item.setattr(data)
            item.save()
            
    except Exception as e:
        #TODO:这里datetime不行
        data = cls.class_transdata(data)
        item=cls(**data)
        try:
            item.save()
        except Exception as e:
            print(e)


#单元测试
class ServiceTestCase(unittest.TestCase):

    def test_douban_book_api(self):
        d=douban_book_api("9787115230270")#9787302150428
        if(d['flag']):
            print(d['isbn'])
        else :
            print(d['error_code'])

if __name__ == '__main__': 
    unittest.main()