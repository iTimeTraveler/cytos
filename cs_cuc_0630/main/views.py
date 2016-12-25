#!/usr/bin/env python
#coding:utf8 

from . import main
from models import Classes,CollegeNews
from flask import render_template

@main.route('/home',methods=['GET','POST'])
def home():
    mainClass = Classes.query.all()
    return render_template('homepage.html',mainClass=mainClass)

@main.route('/enrol_information',methods=['GET','POST'])
def enrol():
    return render_template('secondPages/enrol_information/mainpage.html')

@main.route('/enrol_information/benke',methods=['GET','POST'])
def enrolBenke():
    return render_template('secondPages/enrol_information/recruite-partone.html')

@main.route('/enrol_information/shuoshi',methods=['GET','POST'])
def enrolShuoshi():
    return render_template('secondPages/enrol_information/recruite-parttwo.html')

@main.route('/enrol_information/boshi',methods=['GET','POST'])
def enrolBoshi():
    return render_template('secondPages/enrol_information/recruite-partthree.html')

