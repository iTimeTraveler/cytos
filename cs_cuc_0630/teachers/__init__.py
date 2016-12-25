#!/usr/bin/env python
#coding:utf8

from flask import Blueprint

teachers = Blueprint('teachers',__name__)

from teachers import views
