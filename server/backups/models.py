#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
import datetime
# Create your models here.
#"""备份记录"""
#class BackupRecord(models.Model):
#    version = models.CharField(max_length=128)
#    url = models.URLField(blank=True)#备份的下载地址
#    gtime = models.DateTimeField(auto_now=True)#备份生成时间
#    operator = models.CharField(max_length=32)#操作人姓名
#
#    STATIC_BACKUP_NOTFOUND=unicode(u"备份丢失")
#
#    def gtime_str(self):
#        return self.gtime.strftime("%y/%m/%d %H:%M")
#
#    def delete_url(self):
#        return "/backups/delete/%d"%self.id
#
#    def overide_url(self):
#        return "/backups/overide/%d"%self.id
#
#    def redo_url(self):
#        return "/backups/redo/%d"%self.id
#
#"""还原记录"""
#class RestoreRecord(models.Model):
#    rtime =  models.DateTimeField(auto_now=True)#还原备份的时间
#    version = models.CharField(max_length=128)#还原的版本
#    operator = models.CharField(max_length=32)#操作人姓名
#    rtype = models.CharField(max_length=16)#还原类型,redo或overide
#
#    STATIC_RESTORE_FAILED=unicode(u"还原失败")
#
#    def rtime_str(self):
#        return self.rtime.strftime("%y/%m/%d %H:%M")
#
#    def rtype_str(self):
#        if(self.rtype=='redo'):
#            return unicode(u"增量还原")
#        elif(self.rtype=='overide'):
#            return unicode(u"覆盖")
#
#    def dict(self):
#        return {
#            'rtime':self.rtime_str(),
#            'version':self.version,
#            'operator':self.operator,
#            'rtype':self.rtype_str(),
#        }
#