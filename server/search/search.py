#coding=utf-8
from django.db.models import Q
from models import Index
from models import delzifu
from library.models import Book,Error
import re
import jieba

#简单搜索，分词搜索
def search_easy(text):
	rlist = []
	c = re.match(r"(\d{13}|\d{10})",text.strip())
	if c:
		isbn = c.group(0)
		try:
			b = Book.objects.get(isbn=isbn)
			rlist.append(b)
			return rlist
		except Index.DoesNotExist:
			pass
		except Exception as e:
			error=Error(what='search isbn:"'+isbn+'"error:'+str(e))
			error.save()
			return rlist
	num = 0
	rdict = {}
	words = jieba.cut_for_search(text)
	for w in words:
		w = delzifu(w)
		if w=='':
			continue
		num+=1
		try:
			i = Index.objects.get(index=w)
			q = i.books.all()
		except Index.DoesNotExist:
			continue
		except Exception as e:
			error=Error(what='search:"'+w+'"error:'+str(e))
			error.save()
			return rlist
		for t in q:
			if t.id in rdict:
				rdict[t.id]+=1
			else:
				rdict[t.id]=0
	if not rdict:
		w = delzifu(text)
		if w=='':
			return rlist
		try:
			i = Index.objects.get(index=w)
			q = i.books.all()
		except Index.DoesNotExist:
			return rlist
		except Exception as e:
			error=Error(what='search:"'+w+'"error:'+str(e))
			error.save()
			return rlist
		for t in q:
			rlist.append(t)
		return rlist
	if rdict:
		r = sorted(rdict.iteritems(),key=lambda x:x[1],reverse=True)
		for i in r:
			try:
				rlist.append(Book.objects.get(id=i[0]))
			except Index.DoesNotExist:
				continue
			except Exception as e:
				error=Error(what='sort search:"'+w+'"error:'+str(e))
				error.save()
				return rlist
	return rlist

#深度搜索，分字搜索
def search_deep(text):
	rlist = []
	c = re.match(r"(\d{13}|\d{10})",text.strip())
	if c:
		isbn = c.group(0)
		try:
			b = Book.objects.get(isbn=isbn)
			rlist.append(b)
			return rlist
		except Index.DoesNotExist:
			pass
		except Exception as e:
			error=Error(what='search isbn:"'+isbn+'"error:'+str(e))
			error.save()
			return rlist
	num = 0
	rdict = {}
	words = re.findall(ur"([\u4e00-\u9fa5])|(\w+)",text)
	for w_ in words:
		if w_[0]:
			w = w_[0]
		elif w_[1]:
			w = w_[1]
		w = delzifu(w)
		if w=='':
			continue
		num+=1
		try:
			q = Book.objects.filter(Q(bname__contains=w)|Q(author__contains=w))
		except Index.DoesNotExist:
			continue
		except Exception as e:
			error=Error(what='deep search:"'+w+'"error:'+str(e))
			error.save()
			return rlist
		for t in q:
			if t.id in rdict:
				rdict[t.id]+=1
			else:
				rdict[t.id]=0
	if rdict:
		r = sorted(rdict.iteritems(),key=lambda x:x[1],reverse=True)
		for i in r:
			try:
				rlist.append(Book.objects.get(id=i[0]))
			except Index.DoesNotExist:
				continue
			except Exception as e:
				error=Error(what='sort search:"'+w+'"error:'+str(e))
				error.save()
				return rlist
	return rlist

#搜索时间测试
import datetime
def search_test(text):
	starttime = datetime.datetime.now()
	rlist=search_easy(text)
	endtime = datetime.datetime.now()
	print u'搜索使用时间:'+str(float((endtime-starttime).microseconds)/1000000)+'s'
	return rlist

#搜索方式定义接口
search = search_test