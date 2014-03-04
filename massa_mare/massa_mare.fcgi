#!/usr/bin/python
import sys, os

basepath = '/your/full/home/path'

sys.path.insert(0, basepath + '/.local/lib')
sys.path.insert(0, basepath + '/Sergi/massa_mare')

os.environ['DJANGO_SETTINGS_MODULE'] = 'main.settings'

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method='threaded', daemonize='false')
