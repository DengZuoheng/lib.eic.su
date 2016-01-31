#-*-coding:utf-8-*- 

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django import forms
from django.template import RequestContext

from captcha.fields import CaptchaField
import hashlib
from django.core.urlresolvers import reverse

from library.models import Watcher,Error
from django.conf import settings

class BaseForm(forms.Form):
    account = forms.CharField(label=u'学号:')
    password = forms.CharField(label=u'密码:')
    def clean_password(self):
        password = self.cleaned_data['password']
        num_words = len(password)
        if (num_words < 6) or (num_words >64):
            raise forms.ValidationError(u'密码长度不符!')
        return password

class LoginForm(BaseForm):
    captcha = CaptchaField(label=u'验证码:')
    def clean_account(self):
        account = self.cleaned_data['account']
        if(settings.SUPER_USER==account):
            return account
        num_words = len(account)
        if (num_words==4 or num_words==10):
            pass
        else:
            raise forms.ValidationError(u'学号长度不符!')
        return account

class SignupForm(BaseForm):
    name = forms.CharField(label=u'姓名:')
    lpnumber = forms.CharField(label=u'长号:')
    spnumber = forms.CharField(label=u'短号:')
    captcha = CaptchaField(label=u'验证码:')
    def clean_account(self):
        account = self.cleaned_data['account']
        num_words = len(account)
        if (num_words < 10) or (num_words >10):
            raise forms.ValidationError(u'学号长度不符!')
        try:
            i = Watcher.objects.get(account=account)
        except Watcher.DoesNotExist:
            return account
        except Exception as e:
            error=Error(what=B('find account:"'+account+'"error:'+str(e)))
            error.save()
            raise forms.ValidationError(u'系统故障!')
        raise forms.ValidationError(u'该学号已注册!')
    def clean_name(self):
        name = self.cleaned_data['name']
        num_words = len(name)
        if (num_words == 0) or (num_words >12):
            raise forms.ValidationError(u'姓名长度不符!')
        return name
    def clean_lpnumber(self):
        lpnumber = self.cleaned_data['lpnumber']
        num_words = len(lpnumber)
        if (num_words == 0) or (num_words >12):
            raise forms.ValidationError(u'长号长度不符!')
        return lpnumber
    def clean_spnumber(self):
        spnumber = self.cleaned_data['spnumber']
        num_words = len(spnumber)
        if (num_words == 0) or (num_words >6):
            raise forms.ValidationError(u'短号长度不符!')
        return spnumber


def signup(request):
    if 'account' in request.session:
        return HttpResponseRedirect('/')#已登录
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            account = form.cleaned_data['account']
            #password = form.cleaned_data['password']
            password = hashlib.sha1(form.cleaned_data['password']).hexdigest()
            name = form.cleaned_data['name']
            lpnumber = form.cleaned_data['lpnumber']
            spnumber = form.cleaned_data['spnumber']
            try:
                u = Watcher(account=B(account), password=B(password), name=B(name), lpnumber=B(lpnumber), spnumber=B(spnumber))
                u.save()
            except Exception as e:
                error=Error(what=B('signup:"'+account+'"error:'+str(e)))
                error.save()
            request.session['account'] = account
            return HttpResponseRedirect('/')#注册成功
    else:
        form = SignupForm()
    return render_to_response('signup.html',{'form':form},context_instance = RequestContext(request))

def login(request):
    if 'account' in request.session:
        return HttpResponseRedirect('/')#已登录
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                account = form.cleaned_data['account']
                
                password = hashlib.sha1(form.cleaned_data['password']).hexdigest()
                try:
                    u = Watcher.objects.get(account=account)
                    print u.account
                    if(u.iswatching!=True and u.account!=settings.SUPER_USER):
                        raise Exception(unicode(u'不是当前值班干事!'))
                    if u.password == password:
                        request.session['account'] = account
                        return HttpResponseRedirect('/')#登录成功
                    else:
                       raise Exception(unicode(u'账号或密码错误'))
                except Watcher.DoesNotExist:
                    raise Exception(unicode(u'账号不存在!'))
                except Exception as e:
                    raise Exception(unicode(e))

            except Exception as e:
                error=Error(what=B('account: %s error: %s'%(account,unicode(e))))
                error.save()
            
            return render_to_response('login.html',{'form':form,'error':error.what},context_instance = RequestContext(request))
    else:
        form = LoginForm()
        Watcher.class_checkout_root()
    context={
        'login':True,
        'form':form,
    }
    return render_to_response('login.html',context,context_instance = RequestContext(request))

def logout(request):
    try:
        del request.session['account']
    except:
        #可能是已经退出过的
        pass
    return HttpResponseRedirect('/')#已注销

def modify(request,error_id='0'):
    context={'modify':True,}
    if(error_id!='0'):
        try:
            error=Error.objects.get(id=error_id)
            context['error_item']={
                'what':error.what,
            }
        except Exception as e:
            context['error_item']={
                'what':str(e),
            }

    context['session']=Watcher.class_get_session_name(request.session)
    return render_to_response('modify.html',context,context_instance = RequestContext(request))

def modify_action(request):
    session_id=request.session['account']
    try:
        orig_pw=hashlib.sha1(request.POST['br-input-orig-pw']).hexdigest()
        new_pw=hashlib.sha1(request.POST['br-input-new-pw']).hexdigest()
        confirm_pw=hashlib.sha1(request.POST['br-input-confirm-pw']).hexdigest()
        if(new_pw!=confirm_pw):
            raise Exception(u'新密码与确认密码不一致')

        watcher=Watcher.objects.get(account=session_id)
        if(orig_pw!=watcher.password):
            raise Exception(u'原密码错误')

        watcher.password=new_pw
        watcher.save()
        del request.session['account']
        return HttpResponseRedirect('/account/login/')
    except Exception as e:
        error=Error(what=str(e))
        error.save()
        return HttpResponseRedirect(reverse('login.views.modify', args=[error.id]))

