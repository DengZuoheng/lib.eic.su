#!/usr/bin/env python
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
        ret_dict['byear']=ret_dict['byear'].replace('年','.')
        ret_dict['byear']=ret_dict['byear'].replace('月','.')
        ret_dict['byear']=ret_dict['byear'].replace('日','')
        ret_dict['byear']=ret_dict['byear'].replace('-','.')
        ret_dict['byear']=ret_dict['byear'].replace('/','.')
        ret_dict['price']=ret_dict['price'].replace('元','')
        ret_dict['pagination']=ret_dict['pagination'].replace('页','')
        ret_dict['pagination']=ret_dict['pagination'].replace('p','')
        ret_dict['pagination']=ret_dict['pagination'].replace('P','')
        print(ret_dict['price'])
        try:# 我也不知道豆瓣怎么处理没有译者的情况
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


def search_by(key_word):
    return search_result_example()

def search_result_example():
    return list(Book.objects.all())


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