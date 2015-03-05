# -*- coding: utf-8 -*-
# service就用来封装view层觉得太长的代码吧
import urllib2
import json
import unittest
from library.models import * 

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

def storage(input_file,file_name):
    try:
  
        import sae.storage
        domain_name="images"

        client = sae.storage.Client()
        if(client==None):
            raise Exception("null client")
        obj = sae.storage.Object(input_file.read())
        if(obj==None):
            raise Exception("null object")
        url = client.put(domain_name, file_name, obj) 
        return url

    except Exception as e:
        return unicode(e)

def db_backups_stroage(input_data, file_name=''):
    if(''==file_name):
        import datetime
        now=datetime.datetime.now()
        args=(now.year,now.month,now.day,now.hour,now.minute,now.second)
        file_name="lib.eic.su.backups.%s.%s.%s.%s.%s.%s.json"%args
    try:
        import sae.storage
        domain_name="backups"
        client=sae.storage.Client()
        if(client==None):
            raise Exception("null client")
        obj=sae.storage.Object(input_data)
        if(obj==None):
            raise Exception("null object")
        url=client.put(domain_name,file_name,obj)
        return url
    except Exception as e:
        return unicode(e)

def db_backups():
    
    book_list=[]
    borrower_list=[]
    watcher_list=[]
    borrowrecord_list=[]
    bookingrecord_list=[]
    import json
    try:
        book_list=Watcher.objects.all()
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
            var['book'].append(item.__dict__)
        for item in borrower_list:
            var['borrower'].append(item.__dict__)
        for item in watcher_list:
            var['watcher'].append(item.__dict__)
        for item in borrowrecord_list:
            var['borrowrecord'].append(item.__dict__)
        for item in bookingrecord_list:
            var['bookingrecord'].append(item.__dict__)
        
        return json.dumps(var)
    except Exception as e:
        error=Error(what=unicode(e))
        error.save()
        return json.dumps({'error':error.what,})

def db_restore(backup):
    try:
        
        for item in backup['book']:
            restore_model(item,Book)
        for item in backup['borrower']:
            restore_model(item, Borrower)
        for item in backup['watcher']:
            restore_model(item,Watcher)
        for item in backup['borrowrecord']:
            restore_model(item,BorrowRecord)
        for item in backup['bookingrecord']:
            restore_model(item,BookingRecord)
        return True
    except:
        return False

def restore_model(data,cls):
    try:
        if(hasattr(data,'id')):
            item=cls.objects.get(id=data['id'])
            del data['id']
            for key,value in data:
                setattr(item,key,value)
            item.save()
        else:
            item=cls.objects.get(account=data['account'])
            del data['account']
            for key,value in data:
                setattr(item,key,value)
            item.save()
    except:
        if(hasattr(data,'id')):
            del data['id']
        item=cls(**item)
        item.save()




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