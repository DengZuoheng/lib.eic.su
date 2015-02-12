from django.conf.urls import patterns, url
from views import signup,login,logout

urlpatterns = patterns('',
    url(r'^signup/', signup),
    url(r'^login/', login),
    url(r'^logout/', logout),
)
