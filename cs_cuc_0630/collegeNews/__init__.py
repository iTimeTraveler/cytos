#!/usr/bin/env python
#coding:utf8

from flask import Blueprint

collegeNews = Blueprint('collegeNews',__name__)

from collegeNews import views
