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
        var = library.service.db_backup(request)
        return HttpResponse(json.dumps(var))  
    except Exception as e:
        return HttpResponse(json.dumps({'flag':'false','error':unicode(e)}))  
