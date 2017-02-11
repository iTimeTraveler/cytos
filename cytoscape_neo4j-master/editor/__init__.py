#!/usr/bin/env python
#coding:utf8

from flask import Blueprint

editor = Blueprint('editor',__name__)

from editor import views
