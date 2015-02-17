#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db.models import Q
from models import Index
from models import delzifu
from library.models import Book,Error
import re
import tokenizer

level={
    0:1, #POSTAG_ID_UNKNOW 未知
    10:2, #POSTAG_ID_A      形容词
    20:1, #POSTAG_ID_B      区别词
    30:1, #POSTAG_ID_C      连词
    31:1, #POSTAG_ID_C_N    体词连接
    32:1, #POSTAG_ID_C_Z    分句连接
    40:1, #POSTAG_ID_D      副词
    41:1, #POSTAG_ID_D_B    副词(“不”)
    42:1, #POSTAG_ID_D_M    副词(“没”)
    50:1, #POSTAG_ID_E      叹词
    60:1, #POSTAG_ID_F      方位词
    61:1, #POSTAG_ID_F_S    方位短语(处所词+方位词)
    62:1, #POSTAG_ID_F_N    方位短语(名词+方位词“地上”)
    63:1, #POSTAG_ID_F_V    方位短语(动词+方位词“取前”)
    64:1, #POSTAG_ID_F_Z    方位短语(动词+方位词“取前”)
    70:1, #POSTAG_ID_H      前接成分
    71:1, #POSTAG_ID_H_M    数词前缀(“数”---数十)
    72:1, #POSTAG_ID_H_T    时间词前缀(“公元”“明永乐”)
    73:2, #POSTAG_ID_H_NR   姓氏
    74:2, #POSTAG_ID_H_N    姓氏
    80:1, #POSTAG_ID_K      后接成分
    81:1, #POSTAG_ID_K_M    数词后缀(“来”--,十来个)
    82:2, #POSTAG_ID_K_T    时间词后缀(“初”“末”“时”)
    83:2, #POSTAG_ID_K_N    名词后缀(“们”)
    84:1, #POSTAG_ID_K_S    处所词后缀(“苑”“里”)
    85:1, #POSTAG_ID_K_Z    状态词后缀(“然”)
    86:1, #POSTAG_ID_K_NT   状态词后缀(“然”)
    87:1, #POSTAG_ID_K_NS   状态词后缀(“然”)
    90:2, #POSTAG_ID_M      数词
    95:4, #POSTAG_ID_N      名词
    96:3, #POSTAG_ID_N_RZ   人名(“毛泽东”)
    97:3, #POSTAG_ID_N_T    机构团体(“团”的声母为t，名词代码n和t并在一起。“公司”)
    98:1, #POSTAG_ID_N_TA   ....
    99:2, #POSTAG_ID_N_TZ   机构团体名(“北大”)
    100:3, #POSTAG_ID_N_Z    其他专名(“专”的声母的第1个字母为z，名词代码n和z并在一起。)
    101:3, #POSTAG_ID_NS     名处词
    102:3, #POSTAG_ID_NS_Z   地名(名处词专指：“中国”)
    103:2, #POSTAG_ID_N_M    n-m,数词开头的名词(三个学生)
    104:2, #POSTAG_ID_N_RB   n-rb,以区别词/代词开头的名词(该学校，该生)
    107:1, #POSTAG_ID_O      拟声词
    108:1, #POSTAG_ID_P      介词
    110:1, #POSTAG_ID_Q      量词
    111:1, #POSTAG_ID_Q_V    动量词(“趟”“遍”)
    112:1, #POSTAG_ID_Q_T    时间量词(“年”“月”“期”)
    113:1, #POSTAG_ID_Q_H    货币量词(“元”“美元”“英镑”)
    120:2, #POSTAG_ID_R      代词
    121:1, #POSTAG_ID_R_D    副词性代词(“怎么”)
    122:1, #POSTAG_ID_R_M    数词性代词(“多少”)
    123:1, #POSTAG_ID_R_N    名词性代词(“什么”“谁”)
    124:1, #POSTAG_ID_R_S    处所词性代词(“哪儿”)
    125:1, #POSTAG_ID_R_T    时间词性代词(“何时”)
    126:1, #POSTAG_ID_R_Z    谓词性代词(“怎么样”)
    127:1, #POSTAG_ID_R_B    区别词性代词(“某”“每”)
    130:2, #POSTAG_ID_S      处所词(取英语space的第1个字母。“东部”)
    131:2, #POSTAG_ID_S_Z    处所词(取英语space的第1个字母。“东部”)
    132:3, #POSTAG_ID_T      时间词(取英语time的第1个字母)
    133:3, #POSTAG_ID_T_Z    时间专指(“唐代”“西周”)
    140:1, #POSTAG_ID_U      助词
    141:1, #POSTAG_ID_U_N    定语助词(“的”)
    142:1, #POSTAG_ID_U_D    状语助词(“地”)
    143:1, #POSTAG_ID_U_C    补语助词(“得”)
    144:1, #POSTAG_ID_U_Z    谓词后助词(“了、着、过”)
    145:1, #POSTAG_ID_U_S    体词后助词(“等、等等”)
    146:1, #POSTAG_ID_U_SO   助词(“所”)
    150:1, #POSTAG_ID_W      标点符号
    151:1, #POSTAG_ID_W_D    顿号(“、”)
    152:1, #POSTAG_ID_W_SP   句号(“。”)
    153:1, #POSTAG_ID_W_S    分句尾标点(“，”“；”)
    154:1, #POSTAG_ID_W_L    搭配型标点左部
    155:1, #POSTAG_ID_W_R    搭配型标点右部(“》”“]”“）”)
    156:1, #POSTAG_ID_W_H    中缀型符号
    160:1, #POSTAG_ID_Y      语气词(取汉字“语”的声母。“吗”“吧”“啦”)
    170:3, #POSTAG_ID_V      及物动词(取英语动词verb的第一个字母。)
    171:4, #POSTAG_ID_V_O    不及物谓词(谓宾结构“剃头”)
    172:3, #POSTAG_ID_V_E    动补结构动词(“取出”“放到”)
    173:3, #POSTAG_ID_V_SH   动词“是”
    174:3, #POSTAG_ID_V_YO   动词“有”
    175:2, #POSTAG_ID_V_Q    趋向动词(“来”“去”“进来”)
    176:2, #POSTAG_ID_V_A    助动词(“应该”“能够”)
    180:2, #POSTAG_ID_Z      状态词(不及物动词,v-o、sp之外的不及物动词)
    190:1, #POSTAG_ID_X      语素字
    191:2, #POSTAG_ID_X_N    名词语素(“琥”)
    192:2, #POSTAG_ID_X_V    动词语素(“酹”)
    193:3, #POSTAG_ID_X_S    处所词语素(“中”“日”“美”)
    194:3, #POSTAG_ID_X_T    时间词语素(“唐”“宋”“元”)
    195:2, #POSTAG_ID_X_Z    状态词语素(“伟”“芳”)
    196:2, #POSTAG_ID_X_B    状态词语素(“伟”“芳”)
    200:3, #POSTAG_ID_SP     不及物谓词(主谓结构“腰酸”“头疼”)
    201:2, #POSTAG_ID_MQ     数量短语(“叁个”)
    202:2, #POSTAG_ID_RQ     代量短语(“这个”)
    210:2, #POSTAG_ID_AD     副形词(直接作状语的形容词)
    211:2, #POSTAG_ID_AN     名形词(具有名词功能的形容词)
    212:2, #POSTAG_ID_VD     副动词(直接作状语的动词)
    213:2, #POSTAG_ID_VN     名动词(指具有名词功能的动词)
    230:1, #POSTAG_ID_SPACE  空格
}

#简单搜索，分词搜索
def search_easy(text):
	w = delzifu(text)
	if w=='':
		return rlist
	rlist = []
	c = re.match(r"(\d{13}|\d{10})",text.strip())
	if c:
		isbn = c.group(0)
		try:
			b = Book.objects.get(isbn=isbn)
			rlist.append(b)
			return rlist
		except Index.DoesNotExist:
			return rlist
		except Exception as e:
			error=Error(what='search isbn:"'+isbn+'"error:'+str(e))
			error.save()
			return rlist
	try:
		i = Index.objects.get(index=w)
		q = i.books.all()
		for t in q:
			rlist.append(t)
		return rlist
	except Index.DoesNotExist:
		pass
	except Exception as e:
		error=Error(what='search:"'+w+'"error:'+str(e))
		error.save()
		return rlist
	c = re.search(ur'([\u4e00-\u9fa5]+|\w+)出版社',text)
	if c:
		w = c.group(0)
		try:
			i = Index.objects.get(index=w)
			q = i.books.all()
			for t in q:
				rlist.append(t)
			return rlist
		except Index.DoesNotExist:
			pass
		except Exception as e:
			error=Error(what='search:"'+w+'"error:'+str(e))
			error.save()
			return rlist
	rdict = {}
	words = tokenizer.search(text)
	for w_ in words:
		w = w_[0]
		l = level[int(w_[1])]
		w = delzifu(w)
		if w=='':
			continue
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
				rdict[t.id]+=l
			else:
				rdict[t.id]=l
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
		try:
			q = Book.objects.filter(Q(bname__contains=w)|Q(author__contains=w)|Q(translator__contains=w)|Q(publisher__contains=w))
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
def search(text):
	return search_easy(text.lower())
	#return search_deep(text.lower())
