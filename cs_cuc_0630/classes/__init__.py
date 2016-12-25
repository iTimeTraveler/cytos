#!/usr/bin/env python
#coding:utf8

from flask import Blueprint

classes = Blueprint('classes',__name__)

from classes import views
