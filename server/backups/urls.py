from django.conf.urls import patterns, url
import views
import ajax

urlpatterns = patterns('',
    url(r'^backup/$',views.backup),
    url(r'^restore/$', views.restore),
    url(r'^delete/(\d+)$',views.delete),

    url(r'^RequestAjaxBackup$',ajax.on_backup_request),
    url(r'^PushAjaxRedoFile$',ajax.on_redo_file_push),
    url(r'^PushAjaxOverideFile$',ajax.on_overide_file_push),
    url(r'^PushAjaxRedoID$',ajax.on_redo_id_push),
    url(r'^PushAjaxOverideID$',ajax.on_overide_id_push),

)
