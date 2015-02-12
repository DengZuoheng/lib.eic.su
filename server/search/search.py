#coding=utf-8
from models import Index
from library.models import Book,Error
import jieba
def search(text):
	num = 0
	rdict = {}
	rlist = []
	words = jieba.cut_for_search(text)
	for w in words:
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
	if rdict:
		r = sorted(rdict.iteritems(),key=lambda x:x[1],reverse=True)
		for i in r:
			try:
				rlist.append(Book.objects.get(id=i[0]))
			except Index.DoesNotExist:
				continue
			except Exception as e:
				error=Error(what='search:"'+w+'"error:'+str(e))
				error.save()
				return rlist
	return rlist

def search_deep(text):
	num = 0
	rdict = {}
	rlist = []
	words = re.findall(ur"([\u4e00-\u9fa5])|(\w+)",text)
	for w_ in words:
		if w_[0]:
			w = w_[0]
		elif w_[1]:
			w = w_[1]
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
	if rdict:
		r = sorted(rdict.iteritems(),key=lambda x:x[1],reverse=True)
		for i in r:
			try:
				rlist.append(Book.objects.get(id=i[0]))
			except Index.DoesNotExist:
				continue
			except Exception as e:
				error=Error(what='search:"'+w+'"error:'+str(e))
				error.save()
				return rlist
	return rlist