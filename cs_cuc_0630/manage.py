#!/usr/bin/env python
#coding:utf8

from flask import Flask,url_for,redirect
from flask_script import Manager,Shell
from config import Config
from models import db,CollegeNews,StudentAct,Teachers,Classes
from flask_migrate import Migrate,MigrateCommand


app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app=app)

manager = Manager(app=app)
migrate = Migrate(app,db)

def make_shell_context():
    return dict(app=app,db=db,CollegeNews=CollegeNews,StudentAct=StudentAct,Teachers=Teachers,Classes=Classes)

manager.add_command("shell",Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)

@manager.command
def release():
    app.run(debug=True,port=8887)

from main import main as main_blueprint
app.register_blueprint(blueprint=main_blueprint,url_prefix='/main')
from collegeNews import collegeNews as collegeNews_blueprint
app.register_blueprint(blueprint=collegeNews_blueprint,url_prefix='/collgeNew')
from teachers import teachers as teachers_blueprint
app.register_blueprint(blueprint=teachers_blueprint,url_prefix='/teachers')
from classes import classes as classes_blueprint
app.register_blueprint(blueprint=classes_blueprint,url_prefix='/classes')
from studentAct import studentAct as studentAct_blueprint
app.register_blueprint(blueprint=studentAct_blueprint,url_prefix='/studentAct')


@app.route('/')
def index():
    return redirect(url_for('main.home'))

if __name__ == '__main__':
    manager.run()


