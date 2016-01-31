# -*- coding: utf-8 -*-
# service就用来封装view层觉得太长的代码吧
import urllib2
import json
import unittest
from library.models import * 
from backups.models import *
from server import log

def download_book_info(isbn):
    return douban_book_api(isbn)

def douban_book_api(isbn):
    url='https://api.douban.com/v2/book/isbn/'+str(isbn)
    try:
        socket=urllib2.urlopen(url)
        json_str=socket.read()
        ret=json.loads(json_str)
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
        ret_dict['price']=ret_dict['price'].replace(u'CNY','')
        ret_dict['price']=ret_dict['price'].replace(u' ','')
        ret_dict['pagination']=ret_dict['pagination'].replace(u'页','')
        ret_dict['pagination']=ret_dict['pagination'].replace(u'p','')
        ret_dict['pagination']=ret_dict['pagination'].replace(u'P','')
        log.debug('douban_book_api::douban returned json:',json_str.decode('utf-8'))
        print(ret_dict['price'])
        print(ret_dict['bcover'])
        try:
            ret_dict['translator']=ret['translator']
            ret_dict['bcover']=ret['images']['large']
            log.debug('douban_book_api::before return::ret_dict->',ret_dict)
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
        #使用本地storage
        f = open(file_name,'w')
        f.write(input_data)
        f.close()
        return file_name
        return unicode(e)

def img_upload_storage(input_file, file_name):
    return storage(input_file.read(),file_name,'images')

def db_backup(request):
    # 判断是否是线上
    from os import environ
    online = environ.get("APP_NAME", "") 
    if online:
        from sae.deferredjob import MySQLExport, DeferredJob
        deferred_job = DeferredJob()
        today = datetime.datetime.now().strftime(r'%Y.%m.%d.%H.%M.%S')
        filename = '%s.backup.%s.zip' %(online,today) #用日期作为文件名，并.zip成压缩文件
        job = MySQLExport('backups', filename,'') 
        deferred_job.add(job)
        var = {}
        var['flag]']='true'
        var['online']=online
        var['filename']=filename
        return var
    else:
        return {}


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