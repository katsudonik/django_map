from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '*****', # DB名を設定
        'USER': '*****', # DBへ接続するユーザIDを設定
        'PASSWORD': '*****', # DBへ接続するユーザIDのパスワードを設定
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
        'TEST': {
            'NAME': 'test_sample'
        }
    }
}

REDIS = {
    'default': {
        'host': '127.0.0.1',
        'port': 6379,
        'db': 1,
    }
}

PHANTOM_JS = {
 'path': '/usr/local/bin/phantomjs'
}

#INTERNAL_IPS = ['127.0.0.1', '10.0.2.2']
