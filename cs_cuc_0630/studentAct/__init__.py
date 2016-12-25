#!/usr/bin/env python
#coding:utf8

from flask import Blueprint

studentAct= Blueprint('studentAct',__name__)

from studentAct import views
