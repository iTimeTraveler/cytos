#!/usr/bin/env python
#coding:utf8

from flask import Blueprint

analysis = Blueprint('analysis',__name__)

from analysis import views
