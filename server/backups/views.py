#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django import template
from django.shortcuts import render_to_response
from library.models import * 
from models import *
from django.http import HttpResponse
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import json
import os
from django.views.decorators.csrf import ensure_csrf_cookie


def backup(request):
    session=Watcher.class_get_session_name(request.session)
    if( session==None ):
        return HttpResponseRedirect('/account/login/')
    context = {}
    backup_records = list(BackupRecord.objects.all())
    context = {
        'backups':{'backup':True},
        'session':session,
        "backup_records":backup_records,
    }
    return render_to_response(
        'backup.html',
        context,
        context_instance=RequestContext(request))

def delete(request,backup_id):
    
    backup_record = BackupRecord.objects.get(id=backup_id)
    try:
        os.remove('./library/static/'+backup_record.version)
    except:
        pass
    backup_record.delete()
    return HttpResponseRedirect('/backups/backup')
    

def restore(request):
    session=Watcher.class_get_session_name(request.session)
    if( session==None ):
        return HttpResponseRedirect('/account/login/')
    context = {}
    backup_records = list(BackupRecord.objects.all())
    restore_records = list(RestoreRecord.objects.all())
    context = {
        'backups':{'restore':True},
        'session':session,
        "backup_records":backup_records,
        "restore_records":restore_records,
    }
    return render_to_response(
        'restore.html',
        context,
        context_instance=RequestContext(request))
    pass

def backup_action(request):
    pass

def restore_action(request):
    pass

