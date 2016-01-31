from django.conf.urls import patterns, url
import views
import ajax

urlpatterns = patterns('',
    url(r'^backup/$',views.backup),
    #url(r'^restore/$', views.restore),
    url(r'^delete/(.+)$',views.delete),

    url(r'^RequestAjaxBackup$',ajax.on_backup_request)

)
