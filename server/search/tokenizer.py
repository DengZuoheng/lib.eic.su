#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import urllib,urllib2

from library.models import Error

def cut_for_search(text):
	try:
		_SEGMENT_BASE_URL = 'http://segment.sae.sina.com.cn/urlclient.php'
		payload = urllib.urlencode([('context', text.encode('utf-8')),])
		args = urllib.urlencode([('word_tag', 0), ('encoding', 'UTF-8'),])
		url = _SEGMENT_BASE_URL + '?' + args
		result = urllib2.urlopen(url, payload).read()
		result = json.loads(result)
		for r in result:
			yield r['word']
	except Exception as e:
		error=Error(what='tokenizer:"'+text+'""error:'+str(e))
		error.save()

def search(text):
	try:
		_SEGMENT_BASE_URL = 'http://segment.sae.sina.com.cn/urlclient.php'
		payload = urllib.urlencode([('context', text.encode('utf-8')),])
		args = urllib.urlencode([('word_tag', 1), ('encoding', 'UTF-8'),])
		url = _SEGMENT_BASE_URL + '?' + args
		result = urllib2.urlopen(url, payload).read()
		result = json.loads(result)
		for r in result:
			yield [r['word'],r['word_tag']]
	except Exception as e:
		error=Error(what='tokenizer:"'+text+'""error:'+str(e))
		error.save()