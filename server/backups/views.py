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
from datetime import datetime
import os
from django.views.decorators.csrf import ensure_csrf_cookie


def backup(request):
    session=Watcher.class_get_session_name(request.session)
    if( session==None ):
        return HttpResponseRedirect('/account/login/')
    context = {}
    domain = 'backups'
    try:
        import sae.storage
        client = sae.storage.Client()
        backup_items = client.list(domain)
        backup_records = []
        tf = r'%Y-%m-%d %H:%M:%S'
        for item in backup_items:
            backup_records.append({
                'name':item['name'],
                'datetime':datetime.fromtimestamp(item['datetime']).strftime(tf),
                'url':client.url(domain,item['name']),
                'delete_url':'/backups/delete/%s'%item['name']
                })
    except:
        backup_records = []
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
    domain = 'backups'
    try:
        import sae.storage
        client = sae.storage.Client()
        client.delete(domain,backup_id)
    except:
        pass
    return HttpResponseRedirect('/backups/backup')
    