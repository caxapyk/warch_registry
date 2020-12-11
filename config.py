import os


class Default(object):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or '_WARCH2020_'
