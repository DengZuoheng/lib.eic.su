#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from library.models import * 
from django.http import *
from django.template import RequestContext
from django.core.urlresolvers import reverse
import json
from library import service
import tokenizer
import models
# Create your views here.

def _search(request,start_idx,key_word):
    start_idx=int(start_idx)
    session=Watcher.class_get_session_name(request.session)
    book_list=service.search_by(key_word)
    result={}
    MAX_NO_PAGING=24#如果结果不超过32个,这一页显示完所有结果
    NORMAL_PAGING=12#如果结果超过32个, 这每页16个
    book_list_len=len(book_list)
    try:
        if(0==book_list_len):
            raise Exception('no result')
        result['begin_idx']=start_idx
        result['total']=book_list_len
        if(start_idx==1):
            if(book_list_len<=MAX_NO_PAGING):
                result['end_idx']=book_list_len
            else:
                result['end_idx']=start_idx+NORMAL_PAGING-1 #1+16=17, 所以应减1
        else:
            if(book_list_len<=start_idx+NORMAL_PAGING):
                result['end_idx']=book_list_len
            else:
                result['end_idx']=start_idx+NORMAL_PAGING-1

        if(book_list_len>MAX_NO_PAGING):
            result['pagination'] = True
            if(start_idx==1):
                url=u'/search/start/1/keyword/'+key_word
                result['prev_page']=url
                result['is_first_page']=True
                url=u'/search/start/17/keyword/'+key_word
                result['next_page']=url
            else:
                url=u'/search/start/'+unicode(start_idx-NORMAL_PAGING)+'/keyword/'+key_word
                result['prev_page']=url
                result['is_first_page']=False
                url=u'/search/start/'+unicode(start_idx+NORMAL_PAGING)+'/keyword/'+key_word
                result['next_page']=url
            #page bar
            result['page_href_list']=[]
            begin_idx=1
            while NORMAL_PAGING <=book_list_len:
                url=u'/search/start/'+unicode(begin_idx)+'/keyword/'+key_word
                result['page_href_list'].append(url)
                if(begin_idx==start_idx):
                    result['current_page']=int((begin_idx)/NORMAL_PAGING)+1
                begin_idx=begin_idx+NORMAL_PAGING
                book_list_len=book_list_len-NORMAL_PAGING

            if(book_list_len>0):
                url=u'/search/start/'+unicode(begin_idx)+'/keyword/'+key_word
                result['page_href_list'].append(url)
                if(begin_idx==start_idx):
                    result['current_page']=int((begin_idx)/NORMAL_PAGING)+1
                    result['is_last_page']=True
                    result['next_page']=url

            result['book_list']=book_list[(result['begin_idx']-1):(result['end_idx'])]
        else:
            result['book_list']=book_list 

        context={
            'result':result,
            'session':session,
        }
    except:
        context={
            'result':{
                'begin_idx':0,
                'end_idx':0,
                'total':0,
            },
            'session':session,
        }

    return render_to_response('search.html',context,context_instance=RequestContext(request))

def segment(request):
    context = request.GET['context']
    word_tag = request.GET['word_tag']
    encoding = request.GET['encoding']
    try:
        result = tokenizer.request_segment_service(context,word_tag,encoding)
    except Exception as e:
        result = unicode('["word":"%s",]'%unicode(e))
    return HttpResponse(result)

def rebuild_index(request):
    models.Index.objects.all().delete()
    all_books = Book.objects.all()
    session=Watcher.class_get_session_name(request.session)
    context={
        'session': session,
        'books':all_books,
    }
    print context
    return render_to_response('rebuild_index.html',context)

def on_ajax_reindexing_book_request(request):
    bid = request.GET.get('id')
    ret = {}
    if not bid:
        ret['flag']=False
    else:
        try:
            bid=int(bid)
            book = Book.objects.get(id=bid)
            models.index_book(book)
            ret['flag']=True
        except Exception as e:
            ret['flag']=False
            ret['id']=bid 
            ret['err_str']=str(e) 
                
    return HttpResponse(json.dumps(ret))

