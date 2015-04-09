# -*- coding: utf-8 -*-
import json
import re
import datetime
from django.http import HttpResponse
import library.service
from models import *
from library.models import *

def on_backup_request(request):
    try:
        backup = library.service.db_backups()
        url = library.service.db_backups_storage(json.dumps(backup))
        operator = Watcher.class_get_session_name(request.session)['name']
        kwargs = {
            'url' :url,
            'version': re.findall(r'([^/]*$)',url)[0],
            'gtime': datetime.datetime.now(),
            'operator': operator,
        }
        backup_record = BackupRecord(**kwargs)
        backup_record.save()
        var={
            "flag":"true",
            'version':backup_record.version,
            'url':backup_record.url,
            'gtime':backup_record.gtime_str(),
            'operator':backup_record.operator,
            'delete_url':backup_record.delete_url(),
        }
        var['flag]']='true'
        return HttpResponse(json.dumps(var))  
    except Exception as e:
        return HttpResponse(json.dumps({'flag':'false','error':unicode(e)}))  

def on_redo_file_push(request):
    input_file=request.FILES['input-file-redo']
    var = {'filename':input_file.name}
    try:
        json_obj = json.loads(input_file.read())
        library.service.backup_redo(json_obj)
        restore_record = RestoreRecord(
            rtime = datetime.datetime.now(),
            version = input_file.name,
            operator = Watcher.class_get_session_name(request.session)['name'],
            rtype = 'redo'
            )
        restore_record.save()
        var['flag']='true'
        var['restore_record']=restore_record.dict()
    except Exception as e:
        var['flag']='false'
        var['exception']=unicode(e)
    return HttpResponse(json.dumps(var))

def on_overide_file_push(request):
    input_file=request.FILES['input-file-overide']
    var = {'filename':input_file.name}
    try:
        json_obj = json.loads(input_file.read())
        library.service.backup_overide(json_obj)
        restore_record = RestoreRecord(
            rtime = datetime.datetime.now(),
            version = input_file.name,
            operator = Watcher.class_get_session_name(request.session)['name'],
            rtype = 'overide'
            )
        restore_record.save()
        var['flag']='true'
        var['restore_record']=restore_record.dict()

    except Exception as e:
        var['flag']='false'
        var['exception']=unicode(e)
    return HttpResponse(json.dumps(var))

def on_redo_id_push(request):
    id=request.POST['id']
    var={}
    try:
        file_name, input_file = library.service.get_backup_by_id(id)
        json_obj = json.loads(input_file.read())
        library.service.backup_redo(json_obj)
        var['flag']='true'
        var['filename']=file_name
        restore_record = RestoreRecord(
            rtime = datetime.datetime.now(),
            version = file_name,
            operator = Watcher.class_get_session_name(request.session)['name'],
            rtype = 'redo'
            )
        restore_record.save()
        var['restore_record']=restore_record.dict()
    except Exception as e:
        var['flag']='false'
        var['exception']=unicode(e)
    return HttpResponse(json.dumps(var))

def on_overide_id_push(request):
    id=request.POST['id']
    var={}
    try:
        file_name, input_file = library.service.get_backup_by_id(id)
        json_obj = json.loads(input_file.read())
        library.service.backup_overide(json_obj)
        var['flag']='true'
        var['filename']=file_name
        restore_record = RestoreRecord(
            rtime = datetime.datetime.now(),
            version = file_name,
            operator = Watcher.class_get_session_name(request.session)['name'],
            rtype = 'overide'
            )
        restore_record.save()
        var['restore_record']=restore_record.dict()
    except Exception as e:
        print(e)
        var['flag']='false'
        var['exception']=unicode(e)
    return HttpResponse(json.dumps(var))