#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
from django.db import models
import log

def B(value):
    return base64.b64encode(value.encode('utf-8'))
 
class CompressedTextField(models.TextField):
    """    model Fields for storing text in a compressed format (bz2 by default)    """
    __metaclass__ = models.SubfieldBase
 
    def to_python(self, value):
        #get value
        if not value:
            return value
        try:
            #log.debug('CompressedTextField.to_python::start to decode',value)
            ret = base64.b64decode(value).decode('utf-8')
            #log.debug('CompressedTextField.to_python::finish to decode',value)
            return ret
        except Exception as e:
            print 'decode',value, 'except',e
            return value

    def from_db_value(self, value, expression, connection, context):
        return self.to_python(value)
 
    def get_prep_value(self, value):
        #set value
        if not value:
            return value
        try:
            ret = base64.b64encode(value.encode('utf-8'))
            return ret
        except Exception as e:
            return value

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)