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
        url = library.service.db_backups_stroage(json.dumps(backup))
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