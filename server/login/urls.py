from django.conf.urls import patterns, url
from views import signup,login,logout,modify,modify_action

urlpatterns = patterns('',
    url(r'^signup/$', signup),
    url(r'^login/$', login),
    url(r'^logout/$', logout),
    url(r'^modify/$',modify),
    url(r'^ModifyAction/$',modify_action),
    url(r'^modify/err/(\d+)$',modify),
)
