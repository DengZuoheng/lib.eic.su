#-*-coding:utf-8-*- 

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django import forms
from django.template import RequestContext

from captcha.fields import CaptchaField
import hashlib

from library.models import Watcher,Error

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
        if('root'==account):
            return account
        num_words = len(account)
        if (num_words!=4 or num_words!=10):
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
            error=Error(what='find account:"'+account+'"error:'+str(e))
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
                u = Watcher(account=account, password=password, name=name, lpnumber=lpnumber, spnumber=spnumber)
                u.save()
            except Exception as e:
                error=Error(what='signup:"'+account+'"error:'+str(e))
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
            account = form.cleaned_data['account']
            password = hashlib.md5(form.cleaned_data['password']).hexdigest()
            password = hashlib.sha1(password).hexdigest()
            try:
                u = Watcher.objects.get(account=account)
                if u.password == password:
                    request.session['account'] = account
                    return HttpResponseRedirect('/')#登录成功
                else:
                   error=u'请检测帐号密码是否填写正确!'
            except Watcher.DoesNotExist:
                error=u'请检测帐号密码是否填写正确!'
            except Exception as e:
                error=Error(what='login:"'+account+'"error:'+str(e))
                error.save()
            return render_to_response('login.html',{'form':form,'error':error},context_instance = RequestContext(request))
    else:
        form = LoginForm()
        Watcher.class_checkout_root()
    context={
        'login':True,
        'form':form,
    }
    return render_to_response('login.html',context,context_instance = RequestContext(request))

def logout(request):
    del request.session['account']
    return HttpResponseRedirect('/')#已注销