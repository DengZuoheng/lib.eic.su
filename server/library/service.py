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