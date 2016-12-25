#!/usr/bin/env python
#coding:utf8 

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'hard to guess string'
    SSL_DISABLE = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    #SQLALCHEMY_DATABASE_URI = 'mysql://cuc_admin:123456@222.31.79.131:3306/computercollege'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/computercollege'
    WTF_CSRF_ENABLED = False
    UPLOAD_FOLDER = './uploads'
