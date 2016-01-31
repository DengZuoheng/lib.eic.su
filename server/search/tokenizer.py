#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import urllib,urllib2
from django.conf import settings

from library.models import Error

def segment(context,word_tag=0,encoding='UTF-8'):
	if not context:
		return
	try:
		result = request_segment_service(context,word_tag,encoding)
		result = json.loads(result)
		if word_tag==0:
			for r in result:
				yield r['word']
		else:
			for r in result:
				yield r
	except Exception as e:
		pass

def request_segment_service(context,word_tag=0,encoding='UTF-8'):
	try:
		import sae.const
		_SEGMENT_BASE_URL = 'http://segment.sae.sina.com.cn/urlclient.php'
		payload = urllib.urlencode([('context', context.encode('utf-8')),])
		args = urllib.urlencode([('word_tag', word_tag), ('encoding', encoding),])
		url = _SEGMENT_BASE_URL + '?' + args
		result = urllib2.urlopen(url, payload)
	except:
		#这相当于给本地调试用的
		#当然, 前提是sae上也跑着一个可运行程序
		_SEGMENT_BASE_URL = '/'.join(['http:/',settings.APP_URL,'search','segment'])
		args = urllib.urlencode([
				('word_tag', word_tag), 
				('encoding', encoding),
				('context',context.encode('utf-8'))
			])
		url = _SEGMENT_BASE_URL + '?' + args
		result = urllib2.urlopen(url)
	result = result.read()
	return result