#!/usr/bin/env python
#coding:utf8

from . import collegeNews
from models import Classes,CollegeNews
from flask import render_template

@collegeNews.route('/college_news',methods=['GET','POST'])
def college_news():
    return render_template('secondPages/college_news/mainpage.html')

@collegeNews.route('/partone',methods=['GET','POST'])
def news_partone():
    news = CollegeNews.query.filter_by(news_sort=u'教务管理').all()
    return render_template('secondPages/college_news/news-partone.html',news=news)

@collegeNews.route('/thirdPage/<collegeNewsID>',methods=['GET','POST'])
def news_thirdPage(collegeNewsID):
    news = CollegeNews.query.filter_by(id = collegeNewsID).first()
    return render_template('thirdPages/college_news.html',news=news)

@collegeNews.route('/parttwo',methods=['GET','POST'])
def news_parttwo():
    news = CollegeNews.query.filter_by(news_sort=u'合作交流').all()
    return render_template('secondPages/college_news/news-parttwo.html',news=news)

@collegeNews.route('/partthree',methods=['GET','POST'])
def news_partthree():
    news = CollegeNews.query.filter_by(news_sort=u'科研成果').all()
    return render_template('secondPages/college_news/news-partthree.html',news=news)


@collegeNews.route('/partfour',methods=['GET','POST'])
def news_partfour():
    news = CollegeNews.query.filter_by(news_sort=u'学术讲座').all()
    return render_template('secondPages/college_news/news-four.html',news=news)



