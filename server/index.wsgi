import os

import sys
app_root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(app_root, 'site-packages/six'))
sys.path.insert(0, os.path.join(app_root, 'site-packages/'))

import sae
from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'server.settings'
application = sae.create_wsgi_app(get_wsgi_application())

#from sae.ext.shell import ShellMiddleware
#application = sae.create_wsgi_app(ShellMiddleware('libeicsu'))