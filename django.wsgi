import os, sys

sys.path.append('/home/ec2-user/django/ciphernotes')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
